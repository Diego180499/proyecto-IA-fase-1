"""Servicio de comunicacion entre Python y SWI-Prolog (pyswip).

Responsabilidad: cargar la base de conocimiento Prolog y ejecutar las
consultas de inferencia (sintomas, diagnostico y descripciones).
"""
from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Dict, List

from pyswip import Prolog

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
