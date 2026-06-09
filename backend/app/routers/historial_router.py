"""Router de historial: GET /api/historial, GET/DELETE /api/historial/{id}."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.schemas.diagnostico_schema import DiagnosticoResponse
from app.services import historial_service

router = APIRouter(prefix="/api/historial", tags=["historial"])


@router.get("", response_model=List[DiagnosticoResponse])
def listar_historial(
    limit: Optional[int] = Query(default=None, ge=1, description="Cantidad maxima de registros"),
    offset: int = Query(default=0, ge=0, description="Registros a omitir desde el inicio"),
) -> List[DiagnosticoResponse]:
    """Retorna todos los diagnosticos registrados (paginacion opcional)."""
    return historial_service.obtener_historial(limit=limit, offset=offset)


@router.get("/{diagnostico_id}", response_model=DiagnosticoResponse)
def obtener_diagnostico(diagnostico_id: str) -> DiagnosticoResponse:
    """Retorna el detalle de un diagnostico por su ID."""
    diagnostico = historial_service.obtener_por_id(diagnostico_id)
    if diagnostico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostico no encontrado.",
        )
    return diagnostico


@router.delete("/{diagnostico_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def eliminar_diagnostico(diagnostico_id: str) -> Response:
    """Elimina un registro del historial por su ID."""
    if not historial_service.eliminar_diagnostico(diagnostico_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostico no encontrado.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
