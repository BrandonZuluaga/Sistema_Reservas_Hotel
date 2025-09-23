"""Carga de configuración de base de datos desde variables de entorno."""

from __future__ import annotations

import os
from typing import Final

from dotenv import load_dotenv


load_dotenv()

DATABASE_URL_ENV_VAR: Final[str] = "DATABASE_URL"


def get_database_url() -> str:
    """Obtiene la URL de conexión desde la variable de entorno DATABASE_URL.

    Retorna la URL o lanza una excepción si no está definida.
    """
    url = os.getenv(DATABASE_URL_ENV_VAR)
    if not url:
        raise RuntimeError(
            "DATABASE_URL no está definida. Configure .env o la variable de entorno."
        )
    return url
