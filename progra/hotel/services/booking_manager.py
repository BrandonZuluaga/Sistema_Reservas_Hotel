from __future__ import annotations

from datetime import date
from typing import Dict, List, Optional, Type

from ..models.room import Room, StandardRoom, SuiteRoom, PremiumRoom
from ..models.reservation import Reservation


class BookingManager:
    """Gestor de reservas en memoria."""

    def __init__(self) -> None:
        self._rooms: List[Room] = []
        self._reservations: Dict[int, Reservation] = {}
        self._next_reservation_id: int = 1
        self._seed_default_rooms()

    # ----- Habitaciones -----
    def _seed_default_rooms(self) -> None:
        if self._rooms:
            return
        self._rooms.extend(
            [
                StandardRoom(101, "Estándar 101", 100.0),
                StandardRoom(102, "Estándar 102", 100.0),
                StandardRoom(103, "Estándar 103", 110.0),
                SuiteRoom(201, "Suite 201", 180.0),
                SuiteRoom(202, "Suite 202", 190.0),
                PremiumRoom(301, "Premium 301", 250.0),
            ]
        )

    def add_room(self, room: Room) -> None:
        self._rooms.append(room)

    def get_room_by_id(self, room_id: int) -> Optional[Room]:
        for room in self._rooms:
            if room.id == room_id:
                return room
        return None

    def list_rooms(self) -> List[Room]:
        return list(self._rooms)

    def list_available_rooms(
        self,
        start: date,
        end: date,
        room_kind: Optional[str] = None,
    ) -> List[Room]:
        """Lista habitaciones disponibles filtrando por tipo opcional.

        room_kind puede ser: "estandar", "suite", "premium" (insensible a mayúsculas).
        """

        kind_map = {
            "estandar": StandardRoom,
            "estándar": StandardRoom,
            "standard": StandardRoom,
            "suite": SuiteRoom,
            "premium": PremiumRoom,
        }

        desired_type: Optional[Type[Room]] = None
        if room_kind:
            desired_type = kind_map.get(room_kind.lower())

        available: List[Room] = []
        for room in self._rooms:
            if desired_type and not isinstance(room, desired_type):
                continue
            if self._is_room_available(room.id, start, end):
                available.append(room)
        return available

    # ----- Reservas -----
    def _is_room_available(self, room_id: int, start: date, end: date) -> bool:
        for r in self._reservations.values():
            if r.room.id == room_id and r.overlaps(start, end):
                return False
        return True

    def create_reservation(
        self,
        guest_name: str,
        room_id: int,
        check_in: date,
        check_out: date,
    ) -> Reservation:
        if check_out <= check_in:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")

        room = self.get_room_by_id(room_id)
        if not room:
            raise ValueError("Habitación no encontrada")

        if not self._is_room_available(room_id, check_in, check_out):
            raise ValueError("La habitación no está disponible para ese rango de fechas")

        reservation = Reservation(
            reservation_id=self._next_reservation_id,
            guest_name=guest_name,
            room=room,
            check_in=check_in,
            check_out=check_out,
        )
        self._reservations[self._next_reservation_id] = reservation
        self._next_reservation_id += 1
        return reservation

    def cancel_reservation(self, reservation_id: int) -> bool:
        if reservation_id in self._reservations:
            del self._reservations[reservation_id]
            return True
        return False

    def get_reservation(self, reservation_id: int) -> Optional[Reservation]:
        return self._reservations.get(reservation_id)

    def list_reservations(self) -> List[Reservation]:
        return list(self._reservations.values())

    def calculate_reservation_cost(self, reservation_id: int) -> float:
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            raise ValueError("Reserva no encontrada")
        return reservation.calculate_total_cost()


