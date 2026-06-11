"""Doctor Byte - Punto de entrada de la API FastAPI.

Sistema experto para el diagnostico de fallas comunes en computadoras.
Motor de inferencia en SWI-Prolog, backend en Python con FastAPI.
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import diagnostico_router, historial_router, sintomas_router, telegram_router
from app.services import prolog_service

load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Carga la base de conocimiento Prolog al iniciar la aplicacion."""
    prolog_service.inicializar_prolog()
    yield


app = FastAPI(
    title="Doctor Byte API",
    description="Sistema experto para el diagnostico de fallas en computadoras.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sintomas_router.router)
app.include_router(diagnostico_router.router)
app.include_router(historial_router.router)
app.include_router(telegram_router.router)
app.include_router(telegram_router.diagnostic_router)


@app.get("/api/health", tags=["health"])
def health_check() -> dict:
    """Health check de la API y del motor Prolog."""
    prolog_ok = prolog_service.health_check()
    return {
        "status": "ok" if prolog_ok else "degraded",
        "api": "ok",
        "prolog": "ok" if prolog_ok else "error",
    }
