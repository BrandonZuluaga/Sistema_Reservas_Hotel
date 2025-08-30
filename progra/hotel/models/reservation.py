from __future__ import annotations

from datetime import date

from .room import Room


class Reservation:
    """Reserva de habitación.

    Encapsula datos mediante propiedades.
    """

    def __init__(
        self,
        reservation_id: int,
        guest_name: str,
        room: Room,
        check_in: date,
        check_out: date,
    ) -> None:
        if check_out <= check_in:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")

        self._reservation_id: int = reservation_id
        self._guest_name: str = guest_name
        self._room: Room = room
        self._check_in: date = check_in
        self._check_out: date = check_out

    @property
    def reservation_id(self) -> int:
        return self._reservation_id

    @property
    def guest_name(self) -> str:
        return self._guest_name

    @property
    def room(self) -> Room:
        return self._room

    @property
    def check_in(self) -> date:
        return self._check_in

    @property
    def check_out(self) -> date:
        return self._check_out

    def num_nights(self) -> int:
        return (self._check_out - self._check_in).days

    def calculate_total_cost(self) -> float:
        return self._room.calculate_price(self.num_nights())

    def overlaps(self, start: date, end: date) -> bool:
        """Devuelve True si [start, end) solapa con [check_in, check_out)."""
        if end <= start:
            return False
        return not (end <= self._check_in or start >= self._check_out)

    def __repr__(self) -> str:
        return (
            f"Reservation(id={self._reservation_id}, guest='{self._guest_name}', "
            f"room={self._room.id}, check_in={self._check_in}, check_out={self._check_out})"
        )


