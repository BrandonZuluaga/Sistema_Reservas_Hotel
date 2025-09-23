"""Sesión y motor de SQLAlchemy para conexión a la base de datos."""

from __future__ import annotations

from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .config import get_database_url


def create_sqlalchemy_engine():
    """Crea el motor de SQLAlchemy a partir de la URL configurada."""
    return create_engine(get_database_url(), pool_pre_ping=True, future=True)


engine = create_sqlalchemy_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session() -> Iterator[Session]:
    """Proveedor de sesiones para contextos controlados manualmente."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
