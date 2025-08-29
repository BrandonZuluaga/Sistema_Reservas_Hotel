from __future__ import annotations

from abc import ABC, abstractmethod


class Room(ABC):
    """Base de habitación.

    Aplica encapsulamiento mediante atributos protegidos y propiedades.
    Las subclases implementan polimorfismo en `calculate_price`.
    """

    def __init__(self, room_id: int, name: str, base_rate: float) -> None:
        self._id: int = room_id
        self._name: str = name
        self._base_rate: float = float(base_rate)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_rate(self) -> float:
        return self._base_rate

    @abstractmethod
    def calculate_price(self, num_nights: int) -> float:
        """Calcula el precio total para un número de noches."""
        raise NotImplementedError

    def __repr__(self) -> str:  # útil para debug y listados
        return f"{self.__class__.__name__}(id={self._id}, name='{self._name}', base_rate={self._base_rate})"


class StandardRoom(Room):
    """Habitación estándar: precio lineal por noche."""

    def calculate_price(self, num_nights: int) -> float:
        if num_nights <= 0:
            return 0.0
        return self.base_rate * num_nights


class SuiteRoom(Room):
    """Suite: recargo moderado por servicios adicionales."""

    def calculate_price(self, num_nights: int) -> float:
        if num_nights <= 0:
            return 0.0
        service_multiplier: float = 1.15  # 15% extra
        return self.base_rate * num_nights * service_multiplier


class PremiumRoom(Room):
    """Premium: mayor recargo + tarifa fija de concierge.

    Ejemplo de polimorfismo con lógica distinta a Standard/Suite.
    """

    def calculate_price(self, num_nights: int) -> float:
        if num_nights <= 0:
            return 0.0
        service_multiplier: float = 1.30  # 30% extra
        concierge_fixed_fee: float = 50.0
        return self.base_rate * num_nights * service_multiplier + concierge_fixed_fee


