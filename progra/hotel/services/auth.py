from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Genera el hash de una contraseña en texto plano."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return pwd_context.verify(plain_password, password_hash)


def create_user(
    session: Session,
    *,
    username: str,
    email: str,
    password: str,
    actor_id: uuid.UUID,
) -> User:
    """Crea un usuario activo con contraseña hasheada."""
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        is_active=True,
        id_usuario_creacion=actor_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Obtiene un usuario por su nombre de usuario o None."""
    stmt = select(User).where(User.username == username)
    return session.execute(stmt).scalars().first()


def authenticate_user(
    session: Session, *, username: str, password: str
) -> Optional[User]:
    """Autentica un usuario. Devuelve el usuario si es válido, en otro caso None."""
    user = get_user_by_username(session, username)
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    user.last_login_at = datetime.utcnow()
    user.id_usuario_edicion = user.id
    session.add(user)
    session.commit()
    session.refresh(user)
    return user