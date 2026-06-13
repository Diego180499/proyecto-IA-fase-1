"""Pruebas del servicio de orquestacion del diagnostico."""
import pytest

from app.services import diagnostico_service


def test_validar_sintomas():
    assert diagnostico_service.validar_sintomas(["pantalla_negra"]) is True
    assert diagnostico_service.validar_sintomas([]) is False
    assert diagnostico_service.validar_sintomas(["no_existe"]) is False


def test_sintomas_invalidos():
    invalidos = diagnostico_service.sintomas_invalidos(["pantalla_negra", "no_existe"])
    assert invalidos == ["no_existe"]


def test_procesar_diagnostico_estructura():
    respuesta = diagnostico_service.procesar_diagnostico(["sin_sonido"])
    assert respuesta.id
    assert respuesta.timestamp.endswith("Z")
    assert respuesta.sintomas_ingresados == ["sin_sonido"]
    ids_fallas = {f.id for f in respuesta.fallas_detectadas}
    assert "falla_audio" in ids_fallas
    ids_recs = {r.id for r in respuesta.recomendaciones}
    assert "rec_drivers_audio" in ids_recs
    # Cada falla/recomendacion incluye descripcion legible
    assert all(f.descripcion for f in respuesta.fallas_detectadas)
    assert all(r.descripcion for r in respuesta.recomendaciones)
