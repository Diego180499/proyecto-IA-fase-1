"""Router de sintomas y fallas: GET /api/sintomas, GET /api/fallas."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter

from app.schemas.sintoma_schema import FallaOut, SintomaOut
from app.services import prolog_service

router = APIRouter(prefix="/api", tags=["catalogo"])


@router.get("/sintomas", response_model=List[SintomaOut])
def listar_sintomas() -> List[SintomaOut]:
    """Retorna la lista completa de sintomas disponibles con su descripcion."""
    return [SintomaOut(**s) for s in prolog_service.consultar_sintomas()]


@router.get("/fallas", response_model=List[FallaOut])
def listar_fallas() -> List[FallaOut]:
    """Retorna la lista de fallas diagnosticables con su descripcion."""
    return [FallaOut(**f) for f in prolog_service.consultar_fallas()]
