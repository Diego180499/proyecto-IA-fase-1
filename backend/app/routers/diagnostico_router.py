"""Router de diagnostico: POST /api/diagnostico."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.schemas.diagnostico_schema import DiagnosticoRequest, DiagnosticoResponse
from app.services import diagnostico_service

router = APIRouter(prefix="/api", tags=["diagnostico"])


@router.post("/diagnostico", response_model=DiagnosticoResponse, status_code=status.HTTP_201_CREATED)
def crear_diagnostico(peticion: DiagnosticoRequest) -> DiagnosticoResponse:
    """Recibe una lista de sintomas, ejecuta la inferencia Prolog y retorna el diagnostico.

    Valida (RNF-05) que se reciba al menos un sintoma y que todos existan en la
    base de conocimiento antes de ejecutar el motor de inferencia.
    """
    if not peticion.sintomas:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Debe seleccionar al menos un sintoma.",
        )

    invalidos = diagnostico_service.sintomas_invalidos(peticion.sintomas)
    if invalidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sintomas no reconocidos: {', '.join(invalidos)}",
        )

    return diagnostico_service.procesar_diagnostico(peticion.sintomas)
