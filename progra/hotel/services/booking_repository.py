from __future__ import annotations

import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from database.models import (
    Amenity,
    Customer,
    Payment,
    Reservation,
    Room,
    RoomAmenity,
    RoomType,
)


class BookingRepository:
    """Operaciones de lectura/escritura para el dominio de reservas."""

    def _init_(self, session: Session) -> None:
        self.session = session

    def list_room_types(self) -> List[RoomType]:
        stmt = select(RoomType).order_by(RoomType.name)
        return list(self.session.execute(stmt).scalars().all())

    def list_rooms(self) -> List[Room]:
        stmt = select(Room).order_by(Room.number)
        return list(self.session.execute(stmt).scalars().all())

    def list_available_rooms(
        self, start: date, end: date, room_type_id: Optional[uuid.UUID] = None
    ) -> List[Room]:
        sub = (
            select(Reservation.room_id)
            .where(
                and_(
                    Reservation.check_in < end,
                    Reservation.check_out > start,
                    Reservation.status != "cancelled",
                )
            )
            .subquery()
        )
        stmt = select(Room).where(~Room.id.in_(select(sub.c.room_id)))
        if room_type_id:
            stmt = stmt.where(Room.room_type_id == room_type_id)
        stmt = stmt.order_by(Room.number)
        return list(self.session.execute(stmt).scalars().all())

    def create_customer(
        self,
        *,
        full_name: str,
        document_id: str,
        actor_id: uuid.UUID,
        phone: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Customer:
        customer = Customer(
            full_name=full_name,
            document_id=document_id,
            phone=phone,
            email=email,
            id_usuario_creacion=actor_id,
        )
        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)
        return customer

    def create_reservation(
        self,
        *,
        customer_id: uuid.UUID,
        room_id: uuid.UUID,
        check_in: date,
        check_out: date,
        actor_id: uuid.UUID,
    ) -> Reservation:
        reservation = Reservation(
            customer_id=customer_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            status="confirmed",
            id_usuario_creacion=actor_id,
        )
        self.session.add(reservation)
        self.session.commit()
        self.session.refresh(reservation)
        return reservation

    def cancel_reservation(
        self, reservation_id: uuid.UUID, actor_id: uuid.UUID
    ) -> bool:
        reservation = self.session.get(Reservation, reservation_id)
        if not reservation:
            return False
        reservation.status = "cancelled"
        reservation.id_usuario_edicion = actor_id
        self.session.add(reservation)
        self.session.commit()
        return True

    def get_reservation(self, reservation_id: uuid.UUID) -> Optional[Reservation]:
        return self.session.get(Reservation, reservation_id)

    def list_reservations(self) -> List[Reservation]:
        stmt = select(Reservation).order_by(Reservation.check_in.desc())
        return list(self.session.execute(stmt).scalars().all())

    def add_payment(
        self,
        *,
        reservation_id: uuid.UUID,
        amount: float,
        method: str,
        actor_id: uuid.UUID,
    ) -> Payment:
        payment = Payment(
            reservation_id=reservation_id,
            amount=amount,
            method=method,
            status="paid",
            id_usuario_creacion=actor_id,
        )
        self.session.add(payment)
        self.session.commit()
        self.session.refresh(payment)
        return payment