"""Router de fallas: CRUD + relacion falla->recomendacion.

Rutas:
    GET    /api/fallas/detalle                         Lista de fallas con recomendaciones
    GET    /api/fallas/{id}                             Detalle de una falla
    POST   /api/fallas                                  Crear falla
    PUT    /api/fallas/{id}                             Actualizar falla
    DELETE /api/fallas/{id}                             Eliminar falla
    POST   /api/fallas/{id}/recomendaciones             Asociar recomendacion a la falla
    DELETE /api/fallas/{id}/recomendaciones/{rec}       Desasociar recomendacion de la falla

Nota: GET /api/fallas (lista basica) vive en sintomas_router por compatibilidad.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Response, status

from app.routers.conocimiento_errores import traducir
from app.schemas.sintoma_schema import (
    FallaCreate,
    FallaDetalleOut,
    FallaUpdate,
    RecomendacionRef,
)
from app.services import conocimiento_service as kb

router = APIRouter(prefix="/api/fallas", tags=["fallas"])


@router.get("/detalle", response_model=List[FallaDetalleOut])
def listar_fallas_detalle() -> List[FallaDetalleOut]:
    """Retorna todas las fallas con sus recomendaciones asociadas."""
    return [FallaDetalleOut(**f) for f in kb.listar_fallas()]


@router.get("/{falla_id}", response_model=FallaDetalleOut)
def obtener_falla(falla_id: str) -> FallaDetalleOut:
    """Retorna el detalle de una falla por su identificador."""
    try:
        return FallaDetalleOut(**kb.obtener_falla(falla_id))
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc


@router.post("", response_model=FallaDetalleOut, status_code=status.HTTP_201_CREATED)
def crear_falla(peticion: FallaCreate) -> FallaDetalleOut:
    """Crea una nueva falla y, opcionalmente, sus recomendaciones asociadas."""
    try:
        creada = kb.crear_falla(peticion.id, peticion.descripcion, peticion.recomendaciones)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return FallaDetalleOut(**creada)


@router.put("/{falla_id}", response_model=FallaDetalleOut)
def actualizar_falla(falla_id: str, peticion: FallaUpdate) -> FallaDetalleOut:
    """Actualiza la descripcion y/o las recomendaciones asociadas de una falla."""
    try:
        actualizada = kb.actualizar_falla(falla_id, peticion.descripcion, peticion.recomendaciones)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return FallaDetalleOut(**actualizada)


@router.delete("/{falla_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def eliminar_falla(falla_id: str) -> Response:
    """Elimina una falla y sus relaciones (cascada en sintomas que la causaban)."""
    try:
        kb.eliminar_falla(falla_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{falla_id}/recomendaciones", response_model=FallaDetalleOut)
def asociar_recomendacion(falla_id: str, peticion: RecomendacionRef) -> FallaDetalleOut:
    """Asocia una recomendacion existente a la falla (relacion recomendacion/2)."""
    try:
        actualizada = kb.agregar_recomendacion_a_falla(falla_id, peticion.recomendacion_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return FallaDetalleOut(**actualizada)


@router.delete("/{falla_id}/recomendaciones/{rec_id}", response_model=FallaDetalleOut)
def desasociar_recomendacion(falla_id: str, rec_id: str) -> FallaDetalleOut:
    """Elimina la asociacion entre una falla y una recomendacion."""
    try:
        actualizada = kb.quitar_recomendacion_de_falla(falla_id, rec_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return FallaDetalleOut(**actualizada)
