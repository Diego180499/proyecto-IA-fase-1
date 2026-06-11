"""Tests unitarios para telegram_service.

Se mockea httpx.Client para no realizar llamadas reales a la API de Telegram.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.services import telegram_service


# ---------------------------------------------------------------------------
# Helpers de fixtures
# ---------------------------------------------------------------------------

def _mock_response(json_data: dict, status_code: int = 200) -> MagicMock:
    """Crea un mock de httpx.Response con .json() configurado."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = json_data
    return mock


# ---------------------------------------------------------------------------
# Tests: _token()
# ---------------------------------------------------------------------------

def test_token_levanta_error_si_no_configurado(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="TELEGRAM_BOT_TOKEN no esta configurado"):
        telegram_service._token()


def test_token_devuelve_valor_configurado(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:ABC")
    assert telegram_service._token() == "123:ABC"


# ---------------------------------------------------------------------------
# Tests: verificar_bot()
# ---------------------------------------------------------------------------

def test_verificar_bot_ok(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:ABC")

    respuesta_exitosa = {
        "ok": True,
        "result": {"id": 123, "first_name": "DoctorByteBot", "username": "doctorbytebot"},
    }

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = _mock_response(respuesta_exitosa)

    with patch("httpx.Client", return_value=mock_client):
        resultado = telegram_service.verificar_bot()

    assert resultado["username"] == "doctorbytebot"
    assert resultado["id"] == 123


def test_verificar_bot_token_invalido(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token_invalido")

    respuesta_error = {"ok": False, "description": "Unauthorized", "error_code": 401}

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = _mock_response(respuesta_error)

    with patch("httpx.Client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="getMe fallo"):
            telegram_service.verificar_bot()


# ---------------------------------------------------------------------------
# Tests: enviar_mensaje()
# ---------------------------------------------------------------------------

def test_enviar_mensaje_ok(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:ABC")

    respuesta_exitosa = {
        "ok": True,
        "result": {
            "message_id": 42,
            "chat": {"id": 987654321, "type": "private"},
            "text": "Hola desde el chatbot",
            "date": 1700000000,
        },
    }

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = _mock_response(respuesta_exitosa)

    with patch("httpx.Client", return_value=mock_client):
        resultado = telegram_service.enviar_mensaje("987654321", "Hola desde el chatbot")

    assert resultado["message_id"] == 42
    assert resultado["text"] == "Hola desde el chatbot"

    # Verificar que se llamó con el payload correcto
    llamada_args = mock_client.post.call_args
    assert llamada_args[1]["json"]["chat_id"] == "987654321"
    assert llamada_args[1]["json"]["text"] == "Hola desde el chatbot"


def test_enviar_mensaje_chat_id_invalido(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:ABC")

    respuesta_error = {
        "ok": False,
        "error_code": 400,
        "description": "Bad Request: chat not found",
    }

    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = _mock_response(respuesta_error)

    with patch("httpx.Client", return_value=mock_client):
        with pytest.raises(RuntimeError, match="chat not found"):
            telegram_service.enviar_mensaje("chat_invalido", "Hola")


def test_enviar_mensaje_sin_token(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="TELEGRAM_BOT_TOKEN no esta configurado"):
        telegram_service.enviar_mensaje("123", "Hola")
