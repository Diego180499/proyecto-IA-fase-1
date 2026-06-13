# Doctor Byte — Backend (Fase 1)

Sistema experto para el diagnóstico de fallas comunes en computadoras. El
usuario selecciona síntomas y el sistema devuelve un diagnóstico con
recomendaciones. La lógica de inferencia se implementa en **SWI-Prolog** y el
backend en **Python con FastAPI** (puente `pyswip`).

## Estructura

```
proyecto-IA-fase-1/
├── backend/            # API FastAPI
│   ├── main.py         # Punto de entrada (instancia app, routers, health)
│   ├── requirements.txt
│   ├── .env
│   ├── app/
│   │   ├── routers/    # sintomas, diagnostico, historial
│   │   ├── services/   # prolog, diagnostico, historial, telegram (stub Fase 2)
│   │   ├── models/     # modelo de diagnóstico
│   │   ├── schemas/    # esquemas Pydantic
│   │   └── data/       # historial.json (persistencia)
│   └── tests/          # pruebas unitarias
└── prolog/             # Motor de inferencia SWI-Prolog
    ├── base_conocimiento.pl   # sintoma/1, causa/2, recomendacion/2
    ├── descripciones.pl       # descripcion_falla/2, descripcion_recomendacion/2
    ├── reglas.pl              # diagnosticar/3, posible_falla/2, ...
    ├── persistencia.pl        # predicados dinámicos (Mecanismo 1)
    └── main.pl                # consulta los demás .pl
```

## Requisitos

- Python 3.11+
- SWI-Prolog 9.x o superior (accesible en el PATH del sistema)

## Instalación

```bash
cd backend
pip install -r requirements.txt
```

## Ejecución

```bash
cd backend
uvicorn main:app --reload
```

La documentación interactiva queda disponible en `http://127.0.0.1:8000/docs`.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/sintomas` | Lista de síntomas disponibles |
| `GET` | `/api/fallas` | Lista de fallas diagnosticables |
| `POST` | `/api/diagnostico` | Ejecuta la inferencia y retorna el diagnóstico |
| `GET` | `/api/historial` | Historial de diagnósticos (`?limit=&offset=`) |
| `GET` | `/api/historial/{id}` | Detalle de un diagnóstico |
| `DELETE` | `/api/historial/{id}` | Elimina un registro del historial |
| `GET` | `/api/health` | Health check de la API y del motor Prolog |

## Pruebas

```bash
cd backend
python -m pytest
```

## Notas

- La integración con Telegram (`telegram_service.py`) es **deuda técnica de la
  Fase 2** y se incluye como stub.
- El frontend corresponde a una fase posterior.
