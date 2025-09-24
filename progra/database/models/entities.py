"""Entidades ORM para el sistema de hotel con claves UUID y auditoría."""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import AuditMixin, Base, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Usuario del sistema autenticable mediante contraseña hasheada."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    roles: Mapped[List["Role"]] = relationship(
        secondary="user_roles", back_populates="users"
    )


class Role(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Rol de autorización simple (por ejemplo: admin, recepcionista)."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(50), unique=True)

    users: Mapped[List[User]] = relationship(
        secondary="user_roles", back_populates="roles"
    )


class UserRole(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Tabla de asociación Usuario-Rol con id UUID y unicidad compuesta."""

    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), index=True
    )

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role_pair"),)


class Customer(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Cliente que realiza reservas."""

    __tablename__ = "customers"

    full_name: Mapped[str] = mapped_column(String(120), index=True)
    document_id: Mapped[str] = mapped_column(String(40), index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    email: Mapped[Optional[str]] = mapped_column(String(255))

    __table_args__ = (UniqueConstraint("document_id", name="uq_customer_document"),)

    reservations: Mapped[List["Reservation"]] = relationship(back_populates="customer")


class RoomType(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Tipo de habitación con tarifa base."""

    __tablename__ = "room_types"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    base_rate: Mapped[float] = mapped_column(Float)

    rooms: Mapped[List["Room"]] = relationship(back_populates="room_type")


class Room(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Habitación física del hotel."""

    __tablename__ = "rooms"

    number: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    floor: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer, default=2)
    status: Mapped[str] = mapped_column(String(20), default="available")
    room_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("room_types.id", ondelete="RESTRICT")
    )

    room_type: Mapped[RoomType] = relationship(back_populates="rooms")
    reservations: Mapped[List["Reservation"]] = relationship(back_populates="room")
    amenities: Mapped[List["Amenity"]] = relationship(
        secondary="room_amenities", back_populates="rooms"
    )


class Amenity(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Amenidad disponible en habitaciones."""

    __tablename__ = "amenities"

    name: Mapped[str] = mapped_column(String(80), unique=True)

    rooms: Mapped[List[Room]] = relationship(
        secondary="room_amenities", back_populates="amenities"
    )


class RoomAmenity(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Asociación entre habitaciones y amenidades con id UUID y unicidad compuesta."""

    __tablename__ = "room_amenities"

    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), index=True
    )
    amenity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("amenities.id", ondelete="CASCADE"), index=True
    )

    __table_args__ = (
        UniqueConstraint("room_id", "amenity_id", name="uq_room_amenity_pair"),
    )


class Reservation(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Reserva de habitación con validaciones de rango de fechas."""

    __tablename__ = "reservations"

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id", ondelete="RESTRICT")
    )
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="RESTRICT")
    )
    check_in: Mapped[date] = mapped_column(Date)
    check_out: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="confirmed")
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)

    __table_args__ = (
        CheckConstraint("check_out > check_in", name="ck_reservation_dates"),
    )

    customer: Mapped[Customer] = relationship(back_populates="reservations")
    room: Mapped[Room] = relationship(back_populates="reservations")
    payments: Mapped[List["Payment"]] = relationship(back_populates="reservation")


class Payment(UUIDPrimaryKeyMixin, AuditMixin, Base):
    """Pago asociado a una reserva."""

    __tablename__ = "payments"

    reservation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reservations.id", ondelete="CASCADE")
    )
    amount: Mapped[float] = mapped_column(Float)
    method: Mapped[str] = mapped_column(String(20))
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    transaction_ref: Mapped[Optional[str]] = mapped_column(String(120))

    reservation: Mapped[Reservation] = relationship(back_populates="payments")
