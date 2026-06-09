"""Servicio de notificaciones via bot de Telegram.

DEUDA TECNICA - FASE 2.

Se implementara en la Fase 2 consumiendo la API de Telegram Bot.
Este modulo se mantiene como stub para no bloquear el desarrollo actual.
"""
from __future__ import annotations

from app.schemas.diagnostico_schema import DiagnosticoResponse


def enviar_notificacion(diagnostico: DiagnosticoResponse) -> None:
    """(Fase 2) Envia la notificacion del diagnostico via bot de Telegram.

    Pendiente de implementacion en la Fase 2.
    """
    raise NotImplementedError("La integracion con Telegram se implementara en la Fase 2.")
