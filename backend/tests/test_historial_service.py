"""Pruebas del servicio de persistencia del historial."""
import pytest

from app.schemas.diagnostico_schema import DiagnosticoResponse
from app.schemas.sintoma_schema import FallaOut, RecomendacionOut
from app.services import historial_service


@pytest.fixture(autouse=True)
def historial_temporal(tmp_path, monkeypatch):
    """Aisla el archivo de historial usando un archivo temporal por prueba."""
    archivo = tmp_path / "historial.json"
    monkeypatch.setattr(historial_service, "_HISTORIAL_PATH", archivo)
    yield archivo


def _diagnostico(diagnostico_id: str) -> DiagnosticoResponse:
    return DiagnosticoResponse(
        id=diagnostico_id,
        sintomas_ingresados=["pantalla_negra"],
        fallas_detectadas=[FallaOut(id="falla_ram", descripcion="Falla en RAM")],
        recomendaciones=[RecomendacionOut(id="rec_verificar_ram", descripcion="Verificar RAM")],
        timestamp="2026-06-07T10:00:00Z",
    )


def test_guardar_y_obtener_historial():
    historial_service.guardar_diagnostico(_diagnostico("id-1"))
    historial_service.guardar_diagnostico(_diagnostico("id-2"))
    historial = historial_service.obtener_historial()
    assert len(historial) == 2
    # El mas reciente se retorna primero
    assert historial[0].id == "id-2"


def test_obtener_por_id():
    historial_service.guardar_diagnostico(_diagnostico("id-x"))
    encontrado = historial_service.obtener_por_id("id-x")
    assert encontrado is not None
    assert encontrado.id == "id-x"
    assert historial_service.obtener_por_id("inexistente") is None


def test_eliminar_diagnostico():
    historial_service.guardar_diagnostico(_diagnostico("id-del"))
    assert historial_service.eliminar_diagnostico("id-del") is True
    assert historial_service.eliminar_diagnostico("id-del") is False
    assert historial_service.obtener_por_id("id-del") is None


def test_paginacion():
    for i in range(5):
        historial_service.guardar_diagnostico(_diagnostico(f"id-{i}"))
    pagina = historial_service.obtener_historial(limit=2, offset=1)
    assert len(pagina) == 2
