"""Servicio de comunicacion entre Python y SWI-Prolog (pyswip).

Responsabilidad: cargar la base de conocimiento Prolog y ejecutar las
consultas de inferencia (sintomas, diagnostico y descripciones).
"""
from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Dict, List, Tuple

from pyswip import Prolog

# Descripcion de la falla de respaldo (sin_diagnostico). No forma parte del
# catalogo CRUD pero debe existir para enriquecer la respuesta de fallback de
# diagnosticar/3. El backend la reasserta en cada reconstruccion de la base.
FALLBACK_FALLA_ID = "sin_diagnostico"
FALLBACK_FALLA_DESC = "No se pudo determinar una falla a partir de los sintomas"

# Predicados de hechos gestionados por el CRUD (se limpian al reconstruir).
_HECHOS_GESTIONADOS = (
    "sintoma(_)",
    "causa(_, _)",
    "recomendacion(_, _)",
    "descripcion_sintoma(_, _)",
    "descripcion_falla(_, _)",
    "descripcion_recomendacion(_, _)",
)

# Directorio raiz del proyecto: .../proyecto-IA-fase-1
_BASE_DIR = Path(__file__).resolve().parents[3]

# Ruta de la base de conocimiento Prolog (configurable por variable de entorno)
PROLOG_DIR = Path(os.getenv("PROLOG_DIR", _BASE_DIR / "prolog"))

# Archivos .pl que componen la base de conocimiento, en orden de carga
_KNOWLEDGE_FILES = [
    "base_conocimiento.pl",
    "descripciones.pl",
    "reglas.pl",
    "persistencia.pl",
]

_prolog = Prolog()
_initialized = False
_lock = threading.Lock()


def _to_str(valor) -> str:
    """Normaliza un termino devuelto por pyswip a una cadena de Python."""
    if isinstance(valor, bytes):
        return valor.decode("utf-8")
    return str(valor)


def _ruta_prolog(path: Path) -> str:
    """Devuelve la ruta en el formato que espera SWI-Prolog (barras /)."""
    return str(path).replace("\\", "/")


def inicializar_prolog() -> None:
    """Carga los archivos .pl de la base de conocimiento al iniciar la app.

    La carga es idempotente: solo se ejecuta una vez por proceso.
    """
    global _initialized
    with _lock:
        if _initialized:
            return
        for archivo in _KNOWLEDGE_FILES:
            ruta = PROLOG_DIR / archivo
            if not ruta.exists():
                raise FileNotFoundError(f"No se encontro el archivo Prolog: {ruta}")
            _prolog.consult(_ruta_prolog(ruta))
        _initialized = True


def _asegurar_inicializado() -> None:
    if not _initialized:
        inicializar_prolog()


def consultar_sintomas() -> List[Dict[str, str]]:
    """Ejecuta la consulta sintoma(X) y retorna los sintomas con descripcion."""
    _asegurar_inicializado()
    # Se materializa la consulta externa antes de abrir consultas anidadas
    # (pyswip no permite tener mas de una consulta abierta a la vez).
    ids = [_to_str(sol["S"]) for sol in _prolog.query("sintoma(S)")]
    return [{"id": sid, "descripcion": obtener_descripcion_sintoma(sid)} for sid in ids]


def consultar_fallas() -> List[Dict[str, str]]:
    """Retorna la lista de fallas diagnosticables con su descripcion."""
    _asegurar_inicializado()
    ids: List[str] = []
    for sol in _prolog.query("obtener_fallas(Fallas)"):
        ids = [_to_str(f) for f in sol["Fallas"]]
        break
    return [{"id": fid, "descripcion": obtener_descripcion_falla(fid)} for fid in ids]


def ejecutar_diagnostico(sintomas: List[str]) -> Dict[str, List[str]]:
    """Construye y ejecuta diagnosticar/3 con la lista de sintomas dada.

    Retorna un diccionario con las claves ``fallas`` y ``recomendaciones``,
    cada una con la lista de identificadores inferidos por Prolog.
    """
    _asegurar_inicializado()
    lista = "[" + ",".join(sintomas) + "]"
    consulta = f"diagnosticar({lista}, Fallas, Recomendaciones)"
    for sol in _prolog.query(consulta):
        fallas = [_to_str(f) for f in sol["Fallas"]]
        recomendaciones = [_to_str(r) for r in sol["Recomendaciones"]]
        return {"fallas": fallas, "recomendaciones": recomendaciones}
    return {"fallas": [], "recomendaciones": []}


def existe_sintoma(sintoma_id: str) -> bool:
    """Verifica si un identificador de sintoma existe en la base de conocimiento."""
    _asegurar_inicializado()
    return bool(list(_prolog.query(f"sintoma({sintoma_id})")))


def obtener_descripcion_sintoma(sintoma_id: str) -> str:
    """Consulta descripcion_sintoma/2 para un identificador de sintoma."""
    _asegurar_inicializado()
    for sol in _prolog.query(f"descripcion_sintoma({sintoma_id}, D)"):
        return _to_str(sol["D"])
    return sintoma_id


def obtener_descripcion_falla(falla_id: str) -> str:
    """Consulta descripcion_falla/2 para un identificador de falla."""
    _asegurar_inicializado()
    for sol in _prolog.query(f"descripcion_falla({falla_id}, D)"):
        return _to_str(sol["D"])
    return falla_id


def obtener_descripcion_recomendacion(rec_id: str) -> str:
    """Consulta descripcion_recomendacion/2 para un identificador de recomendacion."""
    _asegurar_inicializado()
    for sol in _prolog.query(f"descripcion_recomendacion({rec_id}, D)"):
        return _to_str(sol["D"])
    return rec_id


def health_check() -> bool:
    """Verifica que el motor Prolog responde a una consulta basica."""
    try:
        _asegurar_inicializado()
        return bool(list(_prolog.query("sintoma(_)")))
    except Exception:
        return False


# ----------------------------------------------------------------------------
# Verificacion de existencia de entidades
# ----------------------------------------------------------------------------
def existe_falla(falla_id: str) -> bool:
    """Verifica si una falla existe en la base (tiene descripcion asociada)."""
    _asegurar_inicializado()
    return bool(list(_prolog.query(f"descripcion_falla({falla_id}, _)")))


def existe_recomendacion(rec_id: str) -> bool:
    """Verifica si una recomendacion existe en la base de conocimiento."""
    _asegurar_inicializado()
    return bool(list(_prolog.query(f"descripcion_recomendacion({rec_id}, _)")))


# ----------------------------------------------------------------------------
# Lectura masiva de hechos (usada para sembrar el estado JSON inicial)
# ----------------------------------------------------------------------------
def listar_sintomas_ids() -> List[str]:
    """Retorna los identificadores de todos los sintomas (sintoma/1)."""
    _asegurar_inicializado()
    return [_to_str(sol["S"]) for sol in _prolog.query("sintoma(S)")]


def mapa_descripcion_sintoma() -> Dict[str, str]:
    """Retorna {id_sintoma: descripcion} de descripcion_sintoma/2."""
    _asegurar_inicializado()
    return {_to_str(s["X"]): _to_str(s["D"]) for s in _prolog.query("descripcion_sintoma(X, D)")}


def mapa_descripcion_falla() -> Dict[str, str]:
    """Retorna {id_falla: descripcion} de descripcion_falla/2."""
    _asegurar_inicializado()
    return {_to_str(s["X"]): _to_str(s["D"]) for s in _prolog.query("descripcion_falla(X, D)")}


def mapa_descripcion_recomendacion() -> Dict[str, str]:
    """Retorna {id_recomendacion: descripcion} de descripcion_recomendacion/2."""
    _asegurar_inicializado()
    return {_to_str(s["X"]): _to_str(s["D"]) for s in _prolog.query("descripcion_recomendacion(X, D)")}


def listar_pares_causa() -> List[Tuple[str, str]]:
    """Retorna la lista de pares (sintoma, falla) de causa/2."""
    _asegurar_inicializado()
    return [(_to_str(s["S"]), _to_str(s["F"])) for s in _prolog.query("causa(S, F)")]


def listar_pares_recomendacion() -> List[Tuple[str, str]]:
    """Retorna la lista de pares (falla, recomendacion) de recomendacion/2."""
    _asegurar_inicializado()
    return [(_to_str(s["F"]), _to_str(s["R"])) for s in _prolog.query("recomendacion(F, R)")]


# ----------------------------------------------------------------------------
# Reconstruccion de la base de conocimiento desde el estado del CRUD
# ----------------------------------------------------------------------------
def _escapar_texto(texto: str) -> str:
    """Escapa una cadena para incrustarla con seguridad en un termino Prolog."""
    return texto.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def reconstruir_desde_estado(estado: Dict) -> None:
    """Reemplaza todos los hechos gestionados por los del estado dado.

    Limpia los predicados de hechos (retractall) y vuelve a afirmarlos a partir
    del diccionario de estado del CRUD, manteniendo el motor de inferencia
    sincronizado con la base de conocimiento persistida. La regla de fallback
    (sin_diagnostico) se reasserta siempre para no degradar el diagnostico.
    """
    _asegurar_inicializado()
    with _lock:
        for patron in _HECHOS_GESTIONADOS:
            list(_prolog.query(f"retractall({patron})"))

        for sintoma in estado.get("sintomas", []):
            sid = sintoma["id"]
            _prolog.assertz(f"sintoma({sid})")
            _prolog.assertz(f'descripcion_sintoma({sid}, "{_escapar_texto(sintoma["descripcion"])}")')
            for falla_id in sintoma.get("fallas", []):
                _prolog.assertz(f"causa({sid}, {falla_id})")

        for falla in estado.get("fallas", []):
            fid = falla["id"]
            _prolog.assertz(f'descripcion_falla({fid}, "{_escapar_texto(falla["descripcion"])}")')
            for rec_id in falla.get("recomendaciones", []):
                _prolog.assertz(f"recomendacion({fid}, {rec_id})")

        for recomendacion in estado.get("recomendaciones", []):
            rid = recomendacion["id"]
            _prolog.assertz(
                f'descripcion_recomendacion({rid}, "{_escapar_texto(recomendacion["descripcion"])}")'
            )

        _prolog.assertz(
            f'descripcion_falla({FALLBACK_FALLA_ID}, "{_escapar_texto(FALLBACK_FALLA_DESC)}")'
        )
