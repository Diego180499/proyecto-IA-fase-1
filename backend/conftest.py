"""Configuracion de pytest: asegura que el paquete `app` sea importable."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
