"""Esquemas Pydantic para la peticion y respuesta de diagnostico."""
from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from app.schemas.sintoma_schema import FallaOut, RecomendacionOut


class DiagnosticoRequest(BaseModel):
    """Cuerpo de la peticion POST /api/diagnostico."""

    sintomas: List[str] = Field(
        ...,
        min_length=1,
        description="Lista de identificadores de sintomas seleccionados",
        examples=[["pantalla_negra", "reinicio_inesperado"]],
    )


class DiagnosticoResponse(BaseModel):
    """Respuesta de un diagnostico realizado."""

    id: str = Field(..., description="UUID generado del diagnostico")
    sintomas_ingresados: List[str] = Field(..., description="Sintomas recibidos en la peticion")
    fallas_detectadas: List[FallaOut] = Field(..., description="Fallas inferidas por el motor Prolog")
    recomendaciones: List[RecomendacionOut] = Field(..., description="Recomendaciones asociadas a las fallas")
    timestamp: str = Field(..., description="Marca de tiempo en formato ISO 8601 (UTC)")
