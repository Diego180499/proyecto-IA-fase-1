"""Servicio CRUD de la base de conocimiento.

Gestiona el catalogo de sintomas, fallas y recomendaciones (y sus relaciones)
que alimenta al motor de inferencia Prolog.

Arquitectura:
    - El estado se mantiene en memoria y se persiste en JSON
      (app/data/conocimiento.json). Esta es la fuente de verdad tras el primer
      arranque.
    - En el primer arranque (sin JSON) el estado se siembra a partir de los
      hechos cargados desde los archivos .pl (semilla inicial).
    - Tras cada cambio se reconstruye la base de hechos dinamicos de Prolog
      (assertz/retractall) para mantener la inferencia sincronizada.

Relaciones modeladas:
    - sintoma  -> fallas        (causa/2)
    - falla    -> recomendaciones (recomendacion/2)
"""
from __future__ import annotations

import json
import os
import re
import threading
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from app.services import prolog_service

# Directorio de datos del backend (backend/app/data)
_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
_KB_PATH = Path(os.getenv("CONOCIMIENTO_PATH", _DATA_DIR / "conocimiento.json"))

# Un identificador valido para Prolog: minuscula inicial, luego alfanumerico/_
_PATRON_ID = re.compile(r"^[a-z][a-z0-9_]*$")

# Entidades que no pueden eliminarse para no romper el caso de fallback.
_RECOMENDACIONES_PROTEGIDAS = {"rec_servicio_tecnico"}

_lock = threading.RLock()
_estado: Dict[str, List[dict]] = {"sintomas": [], "fallas": [], "recomendaciones": []}
_inicializado = False


# ----------------------------------------------------------------------------
# Excepciones de dominio (los routers las traducen a codigos HTTP)
# ----------------------------------------------------------------------------
class ConocimientoError(Exception):
    """Error base del servicio de conocimiento."""


class IdInvalido(ConocimientoError):
    """El identificador no cumple el formato requerido."""


class EntidadNoEncontrada(ConocimientoError):
    """La entidad solicitada no existe."""


class EntidadDuplicada(ConocimientoError):
    """Ya existe una entidad con el mismo identificador."""


class ReferenciaInvalida(ConocimientoError):
    """Se referencia una entidad que no existe."""


class OperacionNoPermitida(ConocimientoError):
    """La operacion no esta permitida (p.ej. eliminar una entidad protegida)."""


# ----------------------------------------------------------------------------
# Inicializacion y persistencia
# ----------------------------------------------------------------------------
def inicializar() -> None:
    """Carga el estado desde JSON o lo siembra desde Prolog, y sincroniza."""
    global _inicializado
    with _lock:
        prolog_service.inicializar_prolog()
        if _KB_PATH.exists():
            _cargar()
        else:
            _sembrar_desde_prolog()
            _persistir()
        prolog_service.reconstruir_desde_estado(_estado)
        _inicializado = True


def _asegurar_inicializado() -> None:
    if not _inicializado:
        inicializar()


def _cargar() -> None:
    """Lee el estado desde el archivo JSON."""
    try:
        contenido = _KB_PATH.read_text(encoding="utf-8").strip()
        datos = json.loads(contenido) if contenido else {}
    except (json.JSONDecodeError, OSError):
        datos = {}
    _estado["sintomas"] = datos.get("sintomas", [])
    _estado["fallas"] = datos.get("fallas", [])
    _estado["recomendaciones"] = datos.get("recomendaciones", [])


def _persistir() -> None:
    """Escribe el estado actual al archivo JSON."""
    _KB_PATH.parent.mkdir(parents=True, exist_ok=True)
    _KB_PATH.write_text(
        json.dumps(_estado, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _sembrar_desde_prolog() -> None:
    """Construye el estado inicial a partir de los hechos cargados en Prolog."""
    desc_sintoma = prolog_service.mapa_descripcion_sintoma()
    desc_falla = prolog_service.mapa_descripcion_falla()
    desc_rec = prolog_service.mapa_descripcion_recomendacion()
    sintoma_ids = prolog_service.listar_sintomas_ids()

    fallas_por_sintoma: Dict[str, List[str]] = defaultdict(list)
    for sintoma_id, falla_id in prolog_service.listar_pares_causa():
        fallas_por_sintoma[sintoma_id].append(falla_id)

    recs_por_falla: Dict[str, List[str]] = defaultdict(list)
    for falla_id, rec_id in prolog_service.listar_pares_recomendacion():
        recs_por_falla[falla_id].append(rec_id)

    _estado["sintomas"] = [
        {
            "id": sid,
            "descripcion": desc_sintoma.get(sid, sid),
            "fallas": fallas_por_sintoma.get(sid, []),
        }
        for sid in sintoma_ids
    ]
    _estado["fallas"] = [
        {
            "id": fid,
            "descripcion": descripcion,
            "recomendaciones": recs_por_falla.get(fid, []),
        }
        for fid, descripcion in desc_falla.items()
        if fid != prolog_service.FALLBACK_FALLA_ID
    ]
    _estado["recomendaciones"] = [
        {"id": rid, "descripcion": descripcion} for rid, descripcion in desc_rec.items()
    ]


def _sincronizar() -> None:
    """Persiste el estado y reconstruye la base de hechos de Prolog."""
    _persistir()
    prolog_service.reconstruir_desde_estado(_estado)


# ----------------------------------------------------------------------------
# Utilidades internas
# ----------------------------------------------------------------------------
def _validar_id(identificador: str) -> None:
    if not _PATRON_ID.match(identificador):
        raise IdInvalido(
            "El identificador debe iniciar con minuscula y contener solo "
            "letras minusculas, numeros o guion bajo (ej. 'falla_ram')."
        )


def _validar_descripcion(descripcion: str) -> None:
    if not descripcion or not descripcion.strip():
        raise ConocimientoError("La descripcion no puede estar vacia.")


def _buscar(coleccion: str, identificador: str) -> Optional[dict]:
    return next((e for e in _estado[coleccion] if e["id"] == identificador), None)


def _obtener_o_error(coleccion: str, identificador: str, etiqueta: str) -> dict:
    entidad = _buscar(coleccion, identificador)
    if entidad is None:
        raise EntidadNoEncontrada(f"{etiqueta} no encontrada: {identificador}")
    return entidad


# ----------------------------------------------------------------------------
# CRUD - Sintomas
# ----------------------------------------------------------------------------
def listar_sintomas() -> List[dict]:
    _asegurar_inicializado()
    with _lock:
        return [dict(s) for s in _estado["sintomas"]]


def obtener_sintoma(sintoma_id: str) -> dict:
    _asegurar_inicializado()
    with _lock:
        return dict(_obtener_o_error("sintomas", sintoma_id, "Sintoma"))


def crear_sintoma(sintoma_id: str, descripcion: str, fallas: Optional[List[str]] = None) -> dict:
    _asegurar_inicializado()
    with _lock:
        _validar_id(sintoma_id)
        _validar_descripcion(descripcion)
        if _buscar("sintomas", sintoma_id) is not None:
            raise EntidadDuplicada(f"Ya existe el sintoma: {sintoma_id}")
        fallas_norm = _validar_referencias_fallas(fallas)
        nuevo = {"id": sintoma_id, "descripcion": descripcion.strip(), "fallas": fallas_norm}
        _estado["sintomas"].append(nuevo)
        _sincronizar()
        return dict(nuevo)


def actualizar_sintoma(
    sintoma_id: str,
    descripcion: Optional[str] = None,
    fallas: Optional[List[str]] = None,
) -> dict:
    _asegurar_inicializado()
    with _lock:
        sintoma = _obtener_o_error("sintomas", sintoma_id, "Sintoma")
        if descripcion is not None:
            _validar_descripcion(descripcion)
            sintoma["descripcion"] = descripcion.strip()
        if fallas is not None:
            sintoma["fallas"] = _validar_referencias_fallas(fallas)
        _sincronizar()
        return dict(sintoma)


def eliminar_sintoma(sintoma_id: str) -> None:
    _asegurar_inicializado()
    with _lock:
        _obtener_o_error("sintomas", sintoma_id, "Sintoma")
        _estado["sintomas"] = [s for s in _estado["sintomas"] if s["id"] != sintoma_id]
        _sincronizar()


def agregar_falla_a_sintoma(sintoma_id: str, falla_id: str) -> dict:
    """Crea la relacion causa(sintoma, falla)."""
    _asegurar_inicializado()
    with _lock:
        sintoma = _obtener_o_error("sintomas", sintoma_id, "Sintoma")
        if _buscar("fallas", falla_id) is None:
            raise ReferenciaInvalida(f"La falla referenciada no existe: {falla_id}")
        if falla_id not in sintoma["fallas"]:
            sintoma["fallas"].append(falla_id)
            _sincronizar()
        return dict(sintoma)


def quitar_falla_de_sintoma(sintoma_id: str, falla_id: str) -> dict:
    """Elimina la relacion causa(sintoma, falla)."""
    _asegurar_inicializado()
    with _lock:
        sintoma = _obtener_o_error("sintomas", sintoma_id, "Sintoma")
        if falla_id not in sintoma["fallas"]:
            raise EntidadNoEncontrada(
                f"El sintoma '{sintoma_id}' no esta asociado a la falla '{falla_id}'."
            )
        sintoma["fallas"] = [f for f in sintoma["fallas"] if f != falla_id]
        _sincronizar()
        return dict(sintoma)


# ----------------------------------------------------------------------------
# CRUD - Fallas
# ----------------------------------------------------------------------------
def listar_fallas() -> List[dict]:
    _asegurar_inicializado()
    with _lock:
        return [dict(f) for f in _estado["fallas"]]


def obtener_falla(falla_id: str) -> dict:
    _asegurar_inicializado()
    with _lock:
        return dict(_obtener_o_error("fallas", falla_id, "Falla"))


def crear_falla(
    falla_id: str,
    descripcion: str,
    recomendaciones: Optional[List[str]] = None,
) -> dict:
    _asegurar_inicializado()
    with _lock:
        _validar_id(falla_id)
        _validar_descripcion(descripcion)
        if _buscar("fallas", falla_id) is not None:
            raise EntidadDuplicada(f"Ya existe la falla: {falla_id}")
        recs_norm = _validar_referencias_recomendaciones(recomendaciones)
        nueva = {
            "id": falla_id,
            "descripcion": descripcion.strip(),
            "recomendaciones": recs_norm,
        }
        _estado["fallas"].append(nueva)
        _sincronizar()
        return dict(nueva)


def actualizar_falla(
    falla_id: str,
    descripcion: Optional[str] = None,
    recomendaciones: Optional[List[str]] = None,
) -> dict:
    _asegurar_inicializado()
    with _lock:
        falla = _obtener_o_error("fallas", falla_id, "Falla")
        if descripcion is not None:
            _validar_descripcion(descripcion)
            falla["descripcion"] = descripcion.strip()
        if recomendaciones is not None:
            falla["recomendaciones"] = _validar_referencias_recomendaciones(recomendaciones)
        _sincronizar()
        return dict(falla)


def eliminar_falla(falla_id: str) -> None:
    _asegurar_inicializado()
    with _lock:
        _obtener_o_error("fallas", falla_id, "Falla")
        _estado["fallas"] = [f for f in _estado["fallas"] if f["id"] != falla_id]
        # Cascada: eliminar las relaciones causa que apuntan a esta falla.
        for sintoma in _estado["sintomas"]:
            if falla_id in sintoma["fallas"]:
                sintoma["fallas"] = [f for f in sintoma["fallas"] if f != falla_id]
        _sincronizar()


def agregar_recomendacion_a_falla(falla_id: str, rec_id: str) -> dict:
    """Crea la relacion recomendacion(falla, recomendacion)."""
    _asegurar_inicializado()
    with _lock:
        falla = _obtener_o_error("fallas", falla_id, "Falla")
        if _buscar("recomendaciones", rec_id) is None:
            raise ReferenciaInvalida(f"La recomendacion referenciada no existe: {rec_id}")
        if rec_id not in falla["recomendaciones"]:
            falla["recomendaciones"].append(rec_id)
            _sincronizar()
        return dict(falla)


def quitar_recomendacion_de_falla(falla_id: str, rec_id: str) -> dict:
    """Elimina la relacion recomendacion(falla, recomendacion)."""
    _asegurar_inicializado()
    with _lock:
        falla = _obtener_o_error("fallas", falla_id, "Falla")
        if rec_id not in falla["recomendaciones"]:
            raise EntidadNoEncontrada(
                f"La falla '{falla_id}' no tiene la recomendacion '{rec_id}'."
            )
        falla["recomendaciones"] = [r for r in falla["recomendaciones"] if r != rec_id]
        _sincronizar()
        return dict(falla)


# ----------------------------------------------------------------------------
# CRUD - Recomendaciones
# ----------------------------------------------------------------------------
def listar_recomendaciones() -> List[dict]:
    _asegurar_inicializado()
    with _lock:
        return [dict(r) for r in _estado["recomendaciones"]]


def obtener_recomendacion(rec_id: str) -> dict:
    _asegurar_inicializado()
    with _lock:
        return dict(_obtener_o_error("recomendaciones", rec_id, "Recomendacion"))


def crear_recomendacion(rec_id: str, descripcion: str) -> dict:
    _asegurar_inicializado()
    with _lock:
        _validar_id(rec_id)
        _validar_descripcion(descripcion)
        if _buscar("recomendaciones", rec_id) is not None:
            raise EntidadDuplicada(f"Ya existe la recomendacion: {rec_id}")
        nueva = {"id": rec_id, "descripcion": descripcion.strip()}
        _estado["recomendaciones"].append(nueva)
        _sincronizar()
        return dict(nueva)


def actualizar_recomendacion(rec_id: str, descripcion: str) -> dict:
    _asegurar_inicializado()
    with _lock:
        recomendacion = _obtener_o_error("recomendaciones", rec_id, "Recomendacion")
        _validar_descripcion(descripcion)
        recomendacion["descripcion"] = descripcion.strip()
        _sincronizar()
        return dict(recomendacion)


def eliminar_recomendacion(rec_id: str) -> None:
    _asegurar_inicializado()
    with _lock:
        _obtener_o_error("recomendaciones", rec_id, "Recomendacion")
        if rec_id in _RECOMENDACIONES_PROTEGIDAS:
            raise OperacionNoPermitida(
                f"La recomendacion '{rec_id}' es necesaria para el diagnostico de "
                "respaldo y no puede eliminarse."
            )
        _estado["recomendaciones"] = [
            r for r in _estado["recomendaciones"] if r["id"] != rec_id
        ]
        # Cascada: desligar la recomendacion de todas las fallas.
        for falla in _estado["fallas"]:
            if rec_id in falla["recomendaciones"]:
                falla["recomendaciones"] = [r for r in falla["recomendaciones"] if r != rec_id]
        _sincronizar()


# ----------------------------------------------------------------------------
# Validacion de referencias entre entidades
# ----------------------------------------------------------------------------
def _validar_referencias_fallas(fallas: Optional[List[str]]) -> List[str]:
    if not fallas:
        return []
    normalizadas: List[str] = []
    for falla_id in fallas:
        if _buscar("fallas", falla_id) is None:
            raise ReferenciaInvalida(f"La falla referenciada no existe: {falla_id}")
        if falla_id not in normalizadas:
            normalizadas.append(falla_id)
    return normalizadas


def _validar_referencias_recomendaciones(recomendaciones: Optional[List[str]]) -> List[str]:
    if not recomendaciones:
        return []
    normalizadas: List[str] = []
    for rec_id in recomendaciones:
        if _buscar("recomendaciones", rec_id) is None:
            raise ReferenciaInvalida(f"La recomendacion referenciada no existe: {rec_id}")
        if rec_id not in normalizadas:
            normalizadas.append(rec_id)
    return normalizadas
