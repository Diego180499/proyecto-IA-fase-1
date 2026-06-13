"""Servicio de persistencia del historial de diagnosticos.

Mecanismo 2 del analisis: el historial se gestiona desde Python en un
archivo JSON. Prolog se mantiene puro como motor de inferencia sin estado.
"""
from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import List, Optional

from app.schemas.diagnostico_schema import DiagnosticoResponse

# Directorio de datos del backend (backend/app/data)
_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
_HISTORIAL_PATH = Path(os.getenv("HISTORIAL_PATH", _DATA_DIR / "historial.json"))

_lock = threading.Lock()


def _asegurar_archivo() -> None:
    """Crea el directorio y el archivo de historial si no existen."""
    _HISTORIAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not _HISTORIAL_PATH.exists():
        _HISTORIAL_PATH.write_text("[]", encoding="utf-8")


def _leer_todo() -> List[dict]:
    _asegurar_archivo()
    try:
        contenido = _HISTORIAL_PATH.read_text(encoding="utf-8").strip()
        return json.loads(contenido) if contenido else []
    except (json.JSONDecodeError, OSError):
        return []


def _escribir_todo(registros: List[dict]) -> None:
    _asegurar_archivo()
    _HISTORIAL_PATH.write_text(
        json.dumps(registros, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def guardar_diagnostico(diagnostico: DiagnosticoResponse) -> None:
    """Serializa y persiste un diagnostico al final del historial."""
    with _lock:
        registros = _leer_todo()
        registros.append(diagnostico.model_dump())
        _escribir_todo(registros)


def obtener_historial(limit: Optional[int] = None, offset: int = 0) -> List[DiagnosticoResponse]:
    """Retorna el historial paginado (mas reciente primero)."""
    with _lock:
        registros = _leer_todo()
    registros = list(reversed(registros))
    if offset:
        registros = registros[offset:]
    if limit is not None:
        registros = registros[:limit]
    return [DiagnosticoResponse(**r) for r in registros]


def obtener_por_id(diagnostico_id: str) -> Optional[DiagnosticoResponse]:
    """Busca un diagnostico por su UUID."""
    with _lock:
        registros = _leer_todo()
    for r in registros:
        if r.get("id") == diagnostico_id:
            return DiagnosticoResponse(**r)
    return None


def eliminar_diagnostico(diagnostico_id: str) -> bool:
    """Elimina un registro del historial. Retorna True si existia."""
    with _lock:
        registros = _leer_todo()
        nuevos = [r for r in registros if r.get("id") != diagnostico_id]
        if len(nuevos) == len(registros):
            return False
        _escribir_todo(nuevos)
        return True
