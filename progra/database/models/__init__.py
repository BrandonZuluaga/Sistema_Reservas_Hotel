"""Modelos ORM del dominio del hotel."""

from .entities import (
    User,
    Role,
    UserRole,
    Customer,
    RoomType,
    Room,
    Amenity,
    RoomAmenity,
    Reservation,
    Payment,
)
from ..base import Base
