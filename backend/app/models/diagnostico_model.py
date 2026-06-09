"""Modelo de datos del diagnostico.

Para la Fase 1 la persistencia se realiza en JSON, por lo que el modelo de
dominio se representa con una dataclass simple que serializa hacia/desde dict.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class DiagnosticoModel:
    """Estructura interna de un diagnostico persistido."""

    id: str
    sintomas_ingresados: List[str]
    fallas_detectadas: List[Dict[str, str]] = field(default_factory=list)
    recomendaciones: List[Dict[str, str]] = field(default_factory=list)
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Serializa el modelo a un diccionario."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiagnosticoModel":
        """Reconstruye el modelo desde un diccionario."""
        return cls(
            id=data["id"],
            sintomas_ingresados=data.get("sintomas_ingresados", []),
            fallas_detectadas=data.get("fallas_detectadas", []),
            recomendaciones=data.get("recomendaciones", []),
            timestamp=data.get("timestamp", ""),
        )
