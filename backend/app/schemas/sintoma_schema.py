"""Esquemas Pydantic para sintomas, fallas y recomendaciones."""
from typing import List, Optional

from pydantic import BaseModel, Field

# Identificador valido como atomo Prolog: minuscula inicial + alfanumerico/_
_ID_PATTERN = r"^[a-z][a-z0-9_]*$"


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


# ----------------------------------------------------------------------------
# Esquemas de detalle (incluyen relaciones) para los endpoints CRUD
# ----------------------------------------------------------------------------
class SintomaDetalleOut(BaseModel):
    """Sintoma con las fallas que puede causar (relacion causa/2)."""

    id: str = Field(..., description="Identificador Prolog del sintoma", examples=["pantalla_negra"])
    descripcion: str = Field(..., description="Descripcion legible del sintoma")
    fallas: List[str] = Field(
        default_factory=list,
        description="Identificadores de fallas asociadas al sintoma",
        examples=[["falla_ram", "falla_fuente_poder"]],
    )


class FallaDetalleOut(BaseModel):
    """Falla con sus recomendaciones asociadas (relacion recomendacion/2)."""

    id: str = Field(..., description="Identificador Prolog de la falla", examples=["falla_ram"])
    descripcion: str = Field(..., description="Descripcion legible de la falla")
    recomendaciones: List[str] = Field(
        default_factory=list,
        description="Identificadores de recomendaciones asociadas a la falla",
        examples=[["rec_verificar_ram"]],
    )


# ----------------------------------------------------------------------------
# Esquemas de entrada (crear / actualizar)
# ----------------------------------------------------------------------------
class SintomaCreate(BaseModel):
    """Cuerpo para crear un sintoma."""

    id: str = Field(
        ...,
        pattern=_ID_PATTERN,
        description="Identificador unico (atomo Prolog) del sintoma",
        examples=["sobrecarga_electrica"],
    )
    descripcion: str = Field(..., min_length=1, description="Descripcion legible del sintoma")
    fallas: List[str] = Field(
        default_factory=list,
        description="Fallas que este sintoma puede causar (deben existir)",
    )


class SintomaUpdate(BaseModel):
    """Cuerpo para actualizar un sintoma (campos opcionales)."""

    descripcion: Optional[str] = Field(default=None, min_length=1, description="Nueva descripcion")
    fallas: Optional[List[str]] = Field(
        default=None,
        description="Reemplaza la lista de fallas asociadas (deben existir)",
    )


class FallaCreate(BaseModel):
    """Cuerpo para crear una falla."""

    id: str = Field(
        ...,
        pattern=_ID_PATTERN,
        description="Identificador unico (atomo Prolog) de la falla",
        examples=["falla_lector_dvd"],
    )
    descripcion: str = Field(..., min_length=1, description="Descripcion legible de la falla")
    recomendaciones: List[str] = Field(
        default_factory=list,
        description="Recomendaciones asociadas a la falla (deben existir)",
    )


class FallaUpdate(BaseModel):
    """Cuerpo para actualizar una falla (campos opcionales)."""

    descripcion: Optional[str] = Field(default=None, min_length=1, description="Nueva descripcion")
    recomendaciones: Optional[List[str]] = Field(
        default=None,
        description="Reemplaza la lista de recomendaciones asociadas (deben existir)",
    )


class RecomendacionCreate(BaseModel):
    """Cuerpo para crear una recomendacion."""

    id: str = Field(
        ...,
        pattern=_ID_PATTERN,
        description="Identificador unico (atomo Prolog) de la recomendacion",
        examples=["rec_actualizar_bios"],
    )
    descripcion: str = Field(..., min_length=1, description="Descripcion legible de la recomendacion")


class RecomendacionUpdate(BaseModel):
    """Cuerpo para actualizar una recomendacion."""

    descripcion: str = Field(..., min_length=1, description="Nueva descripcion de la recomendacion")


# ----------------------------------------------------------------------------
# Esquemas para asociar entidades (relaciones)
# ----------------------------------------------------------------------------
class FallaRef(BaseModel):
    """Referencia a una falla para asociarla a un sintoma."""

    falla_id: str = Field(..., description="Identificador de la falla a asociar", examples=["falla_ram"])


class RecomendacionRef(BaseModel):
    """Referencia a una recomendacion para asociarla a una falla."""

    recomendacion_id: str = Field(
        ..., description="Identificador de la recomendacion a asociar", examples=["rec_verificar_ram"]
    )
