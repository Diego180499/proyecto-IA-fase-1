"""Pruebas del endpoint POST /bot/availability."""
from fastapi.testclient import TestClient

from app.services import bot_availability_service
from main import app

client = TestClient(app)


def _restablecer_estado(habilitado: bool = True) -> None:
    while bot_availability_service.esta_habilitado() != habilitado:
        bot_availability_service.alternar_disponibilidad()


def test_alternar_disponibilidad_endpoint():
    _restablecer_estado(True)

    respuesta = client.post("/bot/availability", json={"availability": False})
    assert respuesta.status_code == 200
    assert respuesta.json() == {"availability": False}
    assert bot_availability_service.esta_habilitado() is False

    respuesta = client.post("/bot/availability", json={"availability": True})
    assert respuesta.status_code == 200
    assert respuesta.json() == {"availability": True}
    assert bot_availability_service.esta_habilitado() is True


def test_obtener_disponibilidad_endpoint():
    _restablecer_estado(True)

    respuesta = client.get("/bot")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"availability": True}

    bot_availability_service.alternar_disponibilidad()

    respuesta = client.get("/bot")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"availability": False}
