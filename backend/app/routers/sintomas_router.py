"""Router de sintomas: catalogo + CRUD + relacion sintoma->falla.

Rutas:
    GET    /api/sintomas                       Lista de sintomas
    GET    /api/sintomas/{id}                  Detalle de un sintoma
    POST   /api/sintomas                       Crear sintoma
    PUT    /api/sintomas/{id}                  Actualizar sintoma
    DELETE /api/sintomas/{id}                  Eliminar sintoma
    POST   /api/sintomas/{id}/fallas           Asociar una falla al sintoma
    DELETE /api/sintomas/{id}/fallas/{falla}   Desasociar una falla del sintoma
    GET    /api/fallas                         Lista de fallas (compatibilidad)
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Response, status

from app.routers.conocimiento_errores import traducir
from app.schemas.sintoma_schema import (
    FallaOut,
    FallaRef,
    SintomaCreate,
    SintomaDetalleOut,
    SintomaUpdate,
)
from app.services import conocimiento_service as kb

router = APIRouter(prefix="/api", tags=["catalogo"])


@router.get("/sintomas", response_model=List[SintomaDetalleOut])
def listar_sintomas() -> List[SintomaDetalleOut]:
    """Retorna la lista completa de sintomas con su descripcion y fallas asociadas."""
    return [SintomaDetalleOut(**s) for s in kb.listar_sintomas()]


@router.get("/sintomas/{sintoma_id}", response_model=SintomaDetalleOut)
def obtener_sintoma(sintoma_id: str) -> SintomaDetalleOut:
    """Retorna el detalle de un sintoma por su identificador."""
    try:
        return SintomaDetalleOut(**kb.obtener_sintoma(sintoma_id))
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc


@router.post("/sintomas", response_model=SintomaDetalleOut, status_code=status.HTTP_201_CREATED)
def crear_sintoma(peticion: SintomaCreate) -> SintomaDetalleOut:
    """Crea un nuevo sintoma y, opcionalmente, sus fallas asociadas."""
    try:
        creado = kb.crear_sintoma(peticion.id, peticion.descripcion, peticion.fallas)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return SintomaDetalleOut(**creado)


@router.put("/sintomas/{sintoma_id}", response_model=SintomaDetalleOut)
def actualizar_sintoma(sintoma_id: str, peticion: SintomaUpdate) -> SintomaDetalleOut:
    """Actualiza la descripcion y/o las fallas asociadas de un sintoma."""
    try:
        actualizado = kb.actualizar_sintoma(sintoma_id, peticion.descripcion, peticion.fallas)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return SintomaDetalleOut(**actualizado)


@router.delete("/sintomas/{sintoma_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def eliminar_sintoma(sintoma_id: str) -> Response:
    """Elimina un sintoma de la base de conocimiento."""
    try:
        kb.eliminar_sintoma(sintoma_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/sintomas/{sintoma_id}/fallas", response_model=SintomaDetalleOut)
def asociar_falla(sintoma_id: str, peticion: FallaRef) -> SintomaDetalleOut:
    """Asocia una falla existente al sintoma (relacion causa/2)."""
    try:
        actualizado = kb.agregar_falla_a_sintoma(sintoma_id, peticion.falla_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return SintomaDetalleOut(**actualizado)


@router.delete("/sintomas/{sintoma_id}/fallas/{falla_id}", response_model=SintomaDetalleOut)
def desasociar_falla(sintoma_id: str, falla_id: str) -> SintomaDetalleOut:
    """Elimina la asociacion entre un sintoma y una falla."""
    try:
        actualizado = kb.quitar_falla_de_sintoma(sintoma_id, falla_id)
    except kb.ConocimientoError as exc:
        raise traducir(exc) from exc
    return SintomaDetalleOut(**actualizado)


@router.get("/fallas", response_model=List[FallaOut])
def listar_fallas() -> List[FallaOut]:
    """Lista de fallas (campos basicos). Para detalle use el router de fallas."""
    return [FallaOut(id=f["id"], descripcion=f["descripcion"]) for f in kb.listar_fallas()]
