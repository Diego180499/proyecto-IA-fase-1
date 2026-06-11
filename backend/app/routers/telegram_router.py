"""Router de Telegram: endpoints para enviar mensajes via Bot API.

Rutas expuestas:
    POST /api/telegram/send   → Envía un mensaje a un usuario de Telegram.
    GET  /api/telegram/health → Verifica que el bot esté configurado y activo.
    POST /send_diagnostic     → Envía un mensaje a Telegram (respuesta simple success).
"""
from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter, HTTPException, status

from app.schemas.telegram_schema import (
    SendDiagnosticRequest,
    SendDiagnosticResponse,
    TelegramMessageRequest,
    TelegramMessageResponse,
)
from app.services import telegram_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/telegram", tags=["telegram"])


@router.post(
    "/send",
    response_model=TelegramMessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar mensaje de Telegram",
    description=(
        "Envía un mensaje de texto al usuario identificado por su **chat_id** de Telegram. "
        "El usuario debe haber iniciado conversación con el bot previamente (enviar /start). "
        "La Bot API de Telegram no permite buscar usuarios por número de teléfono; "
        "se requiere el chat_id numérico."
    ),
)
def enviar_mensaje_telegram(peticion: TelegramMessageRequest) -> TelegramMessageResponse:
    """Recibe un chat_id y envía el mensaje indicado al usuario en Telegram."""
    try:
        resultado = telegram_service.enviar_mensaje(peticion.chat_id, peticion.mensaje)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="La solicitud a la API de Telegram superó el tiempo de espera.",
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error de conectividad con la API de Telegram: {exc}",
        ) from exc

    return TelegramMessageResponse(
        ok=True,
        chat_id=peticion.chat_id,
        message_id=resultado.get("message_id"),
        texto_enviado=peticion.mensaje,
        detalle="Mensaje enviado exitosamente.",
    )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Verificar estado del bot de Telegram",
    description="Llama a getMe de la Bot API para confirmar que el token es válido y el bot está activo.",
)
def health_telegram() -> dict:
    """Verifica que TELEGRAM_BOT_TOKEN sea válido y el bot esté operativo."""
    try:
        info = telegram_service.verificar_bot()
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"No se pudo conectar a la API de Telegram: {exc}",
        ) from exc

    return {
        "status": "ok",
        "bot_id": info.get("id"),
        "bot_username": info.get("username"),
        "bot_name": info.get("first_name"),
    }


diagnostic_router = APIRouter(tags=["telegram"])


@diagnostic_router.post(
    "/send_diagnostic",
    response_model=SendDiagnosticResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar mensaje de diagnóstico a Telegram",
    description=(
        "Envía un mensaje de texto al usuario identificado por su **chat_id** de Telegram. "
        "Responde únicamente con un indicador booleano: `success` es `true` si el mensaje se "
        "envió sin errores y `false` si se generó algún error."
    ),
)
def send_diagnostic(peticion: SendDiagnosticRequest) -> SendDiagnosticResponse:
    """Envía un mensaje a Telegram y devuelve si la operación fue exitosa."""
    try:
        telegram_service.enviar_mensaje(peticion.chat_id, peticion.text)
    except (RuntimeError, httpx.HTTPError) as exc:
        logger.error("No se pudo enviar el mensaje a Telegram: %s", exc)
        return SendDiagnosticResponse(success=False)

    return SendDiagnosticResponse(success=True)
