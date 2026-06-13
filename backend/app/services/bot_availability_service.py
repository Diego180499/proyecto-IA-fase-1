"""Servicio para habilitar o deshabilitar el envio de diagnosticos por Telegram."""
from __future__ import annotations

_telegram_habilitado: bool = True


def esta_habilitado() -> bool:
    """Indica si el envio de diagnosticos por Telegram esta activo."""
    return _telegram_habilitado


def alternar_disponibilidad() -> bool:
    """Invierte el estado actual de la bandera y devuelve el nuevo valor."""
    global _telegram_habilitado
    _telegram_habilitado = not _telegram_habilitado
    return _telegram_habilitado
