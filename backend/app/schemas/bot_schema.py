"""Esquemas Pydantic para la disponibilidad del bot de Telegram."""
from __future__ import annotations

from pydantic import BaseModel, Field


class BotAvailabilityRequest(BaseModel):
    """Cuerpo de la peticion POST /bot/availability."""

    availability: bool = Field(
        ...,
        description="Estado de disponibilidad solicitado (el endpoint alterna el valor actual).",
        examples=[True],
    )


class BotAvailabilityResponse(BaseModel):
    """Respuesta del endpoint POST /bot/availability."""

    availability: bool = Field(
        ...,
        description="Nuevo estado de disponibilidad tras alternar la bandera.",
    )
