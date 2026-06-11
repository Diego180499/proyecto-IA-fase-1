"""Servicio de orquestacion del flujo de diagnostico."""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import List

from app.schemas.diagnostico_schema import DiagnosticoResponse
from app.schemas.sintoma_schema import FallaOut, RecomendacionOut
from app.services import historial_service, prolog_service, telegram_service

logger = logging.getLogger(__name__)


def validar_sintomas(sintomas: List[str]) -> bool:
    """Verifica que todos los sintomas recibidos existan en la base de conocimiento."""
    if not sintomas:
        return False
    return all(prolog_service.existe_sintoma(s) for s in sintomas)


def sintomas_invalidos(sintomas: List[str]) -> List[str]:
    """Retorna la lista de sintomas que no existen en la base de conocimiento."""
    return [s for s in sintomas if not prolog_service.existe_sintoma(s)]


def procesar_diagnostico(sintomas: List[str]) -> DiagnosticoResponse:
    """Ejecuta el flujo completo de un diagnostico.

    Llama al motor Prolog, enriquece la respuesta con descripciones legibles,
    genera UUID y timestamp, y persiste el resultado en el historial.
    """
    resultado = prolog_service.ejecutar_diagnostico(sintomas)

    fallas = [
        FallaOut(id=fid, descripcion=prolog_service.obtener_descripcion_falla(fid))
        for fid in resultado["fallas"]
    ]
    recomendaciones = [
        RecomendacionOut(id=rid, descripcion=prolog_service.obtener_descripcion_recomendacion(rid))
        for rid in resultado["recomendaciones"]
    ]

    respuesta = DiagnosticoResponse(
        id=str(uuid.uuid4()),
        sintomas_ingresados=sintomas,
        fallas_detectadas=fallas,
        recomendaciones=recomendaciones,
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    )

    historial_service.guardar_diagnostico(respuesta)

    _notificar_telegram(respuesta)

    return respuesta


def _formatear_diagnostico(respuesta: DiagnosticoResponse) -> str:
    """Convierte un DiagnosticoResponse en un mensaje de texto plano."""
    lineas: List[str] = ["Resultado del diagnostico"]
    lineas.append(f"ID: {respuesta.id}")
    lineas.append(f"Fecha: {respuesta.timestamp}")
    lineas.append("")

    sintomas = ", ".join(respuesta.sintomas_ingresados) or "Ninguno"
    lineas.append(f"Sintomas ingresados: {sintomas}")
    lineas.append("")

    lineas.append("Fallas detectadas:")
    if respuesta.fallas_detectadas:
        for falla in respuesta.fallas_detectadas:
            lineas.append(f"- {falla.descripcion}")
    else:
        lineas.append("- No se detectaron fallas")
    lineas.append("")

    lineas.append("Recomendaciones:")
    if respuesta.recomendaciones:
        for recomendacion in respuesta.recomendaciones:
            lineas.append(f"- {recomendacion.descripcion}")
    else:
        lineas.append("- No hay recomendaciones")

    return "\n".join(lineas)


def _notificar_telegram(respuesta: DiagnosticoResponse) -> None:
    """Envia el resultado del diagnostico a Telegram.

    Un fallo en el envio no debe interrumpir el flujo de diagnostico, por lo
    que cualquier excepcion se registra en el log y se ignora.
    """
    try:
        mensaje = _formatear_diagnostico(respuesta)
        telegram_service.enviar_mensaje(mensaje)
    except Exception:  # noqa: BLE001
        logger.exception("No se pudo enviar el diagnostico a Telegram")
