"""Pruebas del servicio de comunicacion con Prolog."""
from app.services import prolog_service


def test_inicializar_y_consultar_sintomas():
    prolog_service.inicializar_prolog()
    sintomas = prolog_service.consultar_sintomas()
    # RF-05: al menos 15 sintomas
    assert len(sintomas) >= 15
    ids = {s["id"] for s in sintomas}
    assert "pantalla_negra" in ids
    assert all(s["descripcion"] for s in sintomas)


def test_consultar_fallas():
    fallas = prolog_service.consultar_fallas()
    # RF-06: al menos 10 fallas
    assert len(fallas) >= 10
    ids = {f["id"] for f in fallas}
    assert "falla_ram" in ids


def test_ejecutar_diagnostico_con_sintomas_validos():
    resultado = prolog_service.ejecutar_diagnostico(["pantalla_negra", "reinicio_inesperado"])
    assert "falla_ram" in resultado["fallas"]
    assert "rec_verificar_ram" in resultado["recomendaciones"]
    # No debe haber fallas duplicadas (uso de list_to_set en Prolog)
    assert len(resultado["fallas"]) == len(set(resultado["fallas"]))


def test_existe_sintoma():
    assert prolog_service.existe_sintoma("pantalla_negra") is True
    assert prolog_service.existe_sintoma("sintoma_inexistente") is False


def test_descripciones():
    assert prolog_service.obtener_descripcion_falla("falla_ram")
    assert prolog_service.obtener_descripcion_recomendacion("rec_verificar_ram")
    assert prolog_service.obtener_descripcion_sintoma("pantalla_negra")
