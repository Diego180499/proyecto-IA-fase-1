"""Esquemas Pydantic para la integración con Telegram Bot API."""
from __future__ import annotations

from pydantic import BaseModel, Field


class TelegramMessageRequest(BaseModel):
    """Cuerpo de la petición POST /api/telegram/send."""

    chat_id: str | None = Field(
        default=None,
        description=(
            "Chat ID de destino en Telegram. Opcional: si se omite, se usa el "
            "chat_id configurado en el proyecto (TELEGRAM_CHAT_ID)."
        ),
        examples=["123456789"],
    )
    mensaje: str = Field(
        default="Hola desde el chatbot",
        description="Texto del mensaje a enviar. Por defecto: 'Hola desde el chatbot'.",
    )


class TelegramMessageResponse(BaseModel):
    """Respuesta del envío de mensaje por Telegram."""

    ok: bool = Field(..., description="True si el mensaje fue enviado exitosamente")
    chat_id: str = Field(..., description="Chat ID al que se envió el mensaje")
    message_id: int | None = Field(None, description="ID del mensaje enviado por Telegram")
    texto_enviado: str = Field(..., description="Contenido del mensaje enviado")
    detalle: str = Field(..., description="Descripción del resultado de la operación")


class SendDiagnosticRequest(BaseModel):
    """Cuerpo de la petición POST /send_diagnostic."""

    chat_id: str | None = Field(
        default=None,
        description=(
            "Chat ID de destino en Telegram. Opcional: si se omite, se usa el "
            "chat_id configurado en el proyecto (TELEGRAM_CHAT_ID)."
        ),
        examples=["123456789"],
    )
    text: str = Field(
        default="Hola desde el backend",
        description="Texto del mensaje a enviar a Telegram.",
        examples=["Hola desde el backend"],
    )


class SendDiagnosticResponse(BaseModel):
    """Respuesta del endpoint POST /send_diagnostic."""

    success: bool = Field(
        ...,
        description="True si el mensaje se envió sin errores, False si se generó un error.",
    )
