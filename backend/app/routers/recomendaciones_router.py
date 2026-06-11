"""Router de recomendaciones: CRUD del catalogo de recomendaciones.

Rutas:
    GET    /api/recomendaciones          Lista de recomendaciones
    GET    /api/recomendaciones/{id}     Detalle de una recomendacion
    POST   /api/recomendaciones          Crear recomendacion
    PUT    /api/recomendaciones/{id}     Actualizar recomendacion
    DELETE /api/recomendaciones/{id}     Eliminar recomendacion
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Response, status

from app.routers.conocimiento_errores import traducir
from app.schemas.sintoma_schema import (
    RecomendacionCreate,
    RecomendacionOut,
    RecomendacionUpdate,
)
from app.services import conocimiento_service as kb

router = APIRouter(prefix="/api/recomendaciones", tags=["recomendaciones"])


@router.get("", response_model=List[RecomendacionOut])
def listar_recomendaciones() -> List[RecomendacionOut]:
    """Retorna el catalogo completo de recomendaciones."""
    return [RecomendacionOut(**r) for r in kb.listar_recomendaciones()]


@router.get("/{rec_id}", response_model=RecomendacionOut)
def obtener_recomendacion(rec_id: str) -> RecomendacionOut:
    """Retorna el detalle de una recomendacion por su identificador."""
    try:
        return RecomendacionOut(**kb.obtener_recomendacion(rec_id))
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc


@router.post("", response_model=RecomendacionOut, status_code=status.HTTP_201_CREATED)
def crear_recomendacion(peticion: RecomendacionCreate) -> RecomendacionOut:
    """Crea una nueva recomendacion en el catalogo."""
    try:
        creada = kb.crear_recomendacion(peticion.id, peticion.descripcion)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return RecomendacionOut(**creada)


@router.put("/{rec_id}", response_model=RecomendacionOut)
def actualizar_recomendacion(rec_id: str, peticion: RecomendacionUpdate) -> RecomendacionOut:
    """Actualiza la descripcion de una recomendacion."""
    try:
        actualizada = kb.actualizar_recomendacion(rec_id, peticion.descripcion)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return RecomendacionOut(**actualizada)


@router.delete("/{rec_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def eliminar_recomendacion(rec_id: str) -> Response:
    """Elimina una recomendacion y la desliga de todas las fallas (cascada)."""
    try:
        kb.eliminar_recomendacion(rec_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
