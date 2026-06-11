"""Servicio de mensajeria via Telegram Bot API.

Consume la API REST de Telegram directamente con httpx (sin librerias de
terceros especificas de Telegram). Documentacion de referencia:
https://core.telegram.org/bots/api

Requisitos:
- Crear un bot con @BotFather en Telegram -> obtener el token.
- El usuario DEBE enviar /start al bot al menos una vez para que Telegram
  permita que el bot le envie mensajes (restriccion de privacidad de la API).
- El chat_id es el identificador numerico del usuario en Telegram, NO el
  numero de telefono (la Bot API no expone busqueda por telefono).

Variables de entorno requeridas:
    TELEGRAM_BOT_TOKEN  Token del bot, formato: "123456:ABC-DEF..."
"""
from __future__ import annotations

import os
from typing import Any, Dict

import httpx

_TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/{method}"
_TIMEOUT_SEGUNDOS = 10


def _token() -> str:
    """Obtiene el token del bot desde las variables de entorno."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN no esta configurado. "
            "Agrega la variable en el archivo .env del proyecto."
        )
    return token


def _url(method: str) -> str:
    """Construye la URL completa para un metodo de la Bot API."""
    return _TELEGRAM_API_BASE.format(token=_token(), method=method)


def verificar_bot() -> Dict[str, Any]:
    """Verifica que el token sea valido llamando a getMe.

    Returns:
        dict con la informacion del bot (id, first_name, username, etc.).

    Raises:
        RuntimeError: Si el token es invalido o hay error de red.
    """
    url = _url("getMe")
    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.get(url)

    datos = respuesta.json()

    if not datos.get("ok"):
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(f"Telegram getMe fallo: {descripcion}")

    return datos["result"]


def enviar_mensaje(chat_id: str, texto: str) -> Dict[str, Any]:
    """Envia un mensaje de texto a un usuario de Telegram.

    Llama directamente a POST https://api.telegram.org/bot{TOKEN}/sendMessage

    Args:
        chat_id: Identificador numerico del chat del usuario en Telegram.
                 El usuario debe haber iniciado conversacion con el bot
                 previamente (enviando /start al bot).
        texto:   Contenido del mensaje a enviar.

    Returns:
        dict con el objeto Message devuelto por Telegram (message_id, chat, text).

    Raises:
        RuntimeError: Si Telegram devuelve ok=false.
        httpx.TimeoutException: Si la llamada excede _TIMEOUT_SEGUNDOS.
        httpx.RequestError: Si hay un problema de conectividad.
    """
    payload = {
        "chat_id": chat_id,
        "text": texto,
    }

    url = _url("sendMessage")
    with httpx.Client(timeout=_TIMEOUT_SEGUNDOS) as client:
        respuesta = client.post(url, json=payload)

    datos = respuesta.json()

    if not datos.get("ok"):
        codigo = datos.get("error_code", "?")
        descripcion = datos.get("description", "Error desconocido")
        raise RuntimeError(
            f"Telegram sendMessage fallo (codigo {codigo}): {descripcion}"
        )

    return datos["result"]
