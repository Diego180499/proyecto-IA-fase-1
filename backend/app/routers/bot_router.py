"""Router del bot: control de disponibilidad para envio de diagnosticos por Telegram."""
from __future__ import annotations

from fastapi import APIRouter, status

from app.schemas.bot_schema import BotAvailabilityRequest, BotAvailabilityResponse
from app.services import bot_availability_service

router = APIRouter(prefix="/bot", tags=["bot"])


@router.get(
    "",
    response_model=BotAvailabilityResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar envio de diagnosticos por Telegram",
    description=(
        "Retorna el valor actual de la bandera que controla si el bot envia mensajes "
        "de diagnostico a Telegram. `true` indica envio activo; `false` indica envio desactivado."
    ),
)
def obtener_disponibilidad_telegram() -> BotAvailabilityResponse:
    """Retorna el estado actual de la bandera de disponibilidad."""
    return BotAvailabilityResponse(availability=bot_availability_service.esta_habilitado())


@router.post(
    "/availability",
    response_model=BotAvailabilityResponse,
    status_code=status.HTTP_200_OK,
    summary="Alternar envio de diagnosticos por Telegram",
    description=(
        "Invierte el estado de la bandera de disponibilidad: si esta activa la desactiva "
        "y si esta inactiva la activa. El cuerpo de la peticion acepta el campo "
        "`availability` segun el contrato de la API."
    ),
)
def alternar_disponibilidad_telegram(
    _: BotAvailabilityRequest,
) -> BotAvailabilityResponse:
    """Alterna la bandera que controla el envio de diagnosticos por Telegram."""
    nuevo_estado = bot_availability_service.alternar_disponibilidad()
    return BotAvailabilityResponse(availability=nuevo_estado)
