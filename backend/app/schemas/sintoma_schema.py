"""Esquemas Pydantic para sintomas, fallas y recomendaciones."""
from pydantic import BaseModel, Field


class SintomaOut(BaseModel):
    """Sintoma disponible en la base de conocimiento."""

    id: str = Field(..., description="Identificador Prolog del sintoma", examples=["pantalla_negra"])
    descripcion: str = Field(..., description="Descripcion legible del sintoma")


class FallaOut(BaseModel):
    """Falla diagnosticable."""

    id: str = Field(..., description="Identificador Prolog de la falla", examples=["falla_ram"])
    descripcion: str = Field(..., description="Descripcion legible de la falla")


class RecomendacionOut(BaseModel):
    """Recomendacion de solucion asociada a una falla."""

    id: str = Field(..., description="Identificador Prolog de la recomendacion", examples=["rec_verificar_ram"])
    descripcion: str = Field(..., description="Descripcion legible de la recomendacion")
