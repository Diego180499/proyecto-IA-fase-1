"""Servicio de orquestacion del flujo de diagnostico."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List

from app.schemas.diagnostico_schema import DiagnosticoResponse
from app.schemas.sintoma_schema import FallaOut, RecomendacionOut
from app.services import historial_service, prolog_service


def validar_sintomas(sintomas: List[str]) -> bool:
    """Verifica que todos los sintomas recibidos existan en la base de conocimiento."""
    if not sintomas:
        return False
    return all(prolog_service.existe_sintoma(s) for s in sintomas)


def sintomas_invalidos(sintomas: List[str]) -> List[str]:
    """Retorna la lista de sintomas que no existen en la base de conocimiento."""
    return [s for s in sintomas if not prolog_service.existe_sintoma(s)]


def procesar_diagnostico(sintomas: List[str]) -> DiagnosticoResponse:
    """Ejecuta el flujo completo de un diagnostico.

    Llama al motor Prolog, enriquece la respuesta con descripciones legibles,
    genera UUID y timestamp, y persiste el resultado en el historial.
    """
    resultado = prolog_service.ejecutar_diagnostico(sintomas)

    fallas = [
        FallaOut(id=fid, descripcion=prolog_service.obtener_descripcion_falla(fid))
        for fid in resultado["fallas"]
    ]
    recomendaciones = [
        RecomendacionOut(id=rid, descripcion=prolog_service.obtener_descripcion_recomendacion(rid))
        for rid in resultado["recomendaciones"]
    ]

    respuesta = DiagnosticoResponse(
        id=str(uuid.uuid4()),
        sintomas_ingresados=sintomas,
        fallas_detectadas=fallas,
        recomendaciones=recomendaciones,
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )

    historial_service.guardar_diagnostico(respuesta)
    return respuesta
