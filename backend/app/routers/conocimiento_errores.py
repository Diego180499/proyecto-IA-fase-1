"""Traduccion de excepciones del servicio de conocimiento a HTTPException."""
from __future__ import annotations

from fastapi import HTTPException, status

from app.services import conocimiento_service as kb


def traducir(exc: kb.ConocimientoError) -> HTTPException:
    """Mapea una excepcion de dominio al codigo HTTP correspondiente."""
    if isinstance(exc, kb.EntidadNoEncontrada):
        codigo = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, kb.EntidadDuplicada):
        codigo = status.HTTP_409_CONFLICT
    elif isinstance(exc, kb.OperacionNoPermitida):
        codigo = status.HTTP_409_CONFLICT
    elif isinstance(exc, kb.ReferenciaInvalida):
        codigo = status.HTTP_400_BAD_REQUEST
    elif isinstance(exc, kb.IdInvalido):
        codigo = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        codigo = status.HTTP_400_BAD_REQUEST
    return HTTPException(status_code=codigo, detail=str(exc))
