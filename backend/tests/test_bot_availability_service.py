"""Pruebas del servicio de disponibilidad del bot de Telegram."""
from app.services import bot_availability_service


def _restablecer_estado(habilitado: bool = True) -> None:
    """Fija la bandera al estado indicado para pruebas aisladas."""
    while bot_availability_service.esta_habilitado() != habilitado:
        bot_availability_service.alternar_disponibilidad()


def test_esta_habilitado_por_defecto():
    _restablecer_estado(True)
    assert bot_availability_service.esta_habilitado() is True


def test_alternar_disponibilidad():
    _restablecer_estado(True)
    assert bot_availability_service.alternar_disponibilidad() is False
    assert bot_availability_service.esta_habilitado() is False
    assert bot_availability_service.alternar_disponibilidad() is True
    assert bot_availability_service.esta_habilitado() is True
