from __future__ import annotations

from datetime import date
from typing import Optional

from hotel.services import BookingManager


def parse_date(input_str: str) -> Optional[date]:
    try:
        y, m, d = map(int, input_str.split("-"))
        return date(y, m, d)
    except Exception:
        return None


def show_main_menu() -> None:
    print("\n=== Sistema de Reservas de Hotel ===")
    print("1. Listar habitaciones")
    print("2. Listar habitaciones disponibles por rango y tipo")
    print("3. Crear reserva")
    print("4. Listar reservas")
    print("5. Calcular costo de una reserva")
    print("6. Cancelar reserva")
    print("0. Salir")


def main() -> None:
    manager = BookingManager()

    while True:
        show_main_menu()
        option = input("Seleccione una opción: ").strip()

        if option == "1":
            rooms = manager.list_rooms()
            print("\nHabitaciones:")
            for r in rooms:
                print(f"- {r.id} | {r.name} | Base: ${r.base_rate:.2f} | Tipo: {r.__class__.__name__}")

        elif option == "2":
            start_str = input("Fecha inicio (YYYY-MM-DD): ").strip()
            end_str = input("Fecha fin (YYYY-MM-DD): ").strip()
            kind = input("Tipo (estandar/suite/premium o vacío para todas): ").strip()
            start = parse_date(start_str)
            end = parse_date(end_str)
            if not start or not end or end <= start:
                print("Fechas inválidas")
                continue
            available = manager.list_available_rooms(start, end, kind if kind else None)
            print("\nDisponibles:")
            for r in available:
                print(f"- {r.id} | {r.name} | Base: ${r.base_rate:.2f} | Tipo: {r.__class__.__name__}")
            if not available:
                print("(No hay habitaciones disponibles)")

        elif option == "3":
            guest = input("Nombre del huésped: ").strip()
            room_id_str = input("ID de la habitación: ").strip()
            start_str = input("Check-in (YYYY-MM-DD): ").strip()
            end_str = input("Check-out (YYYY-MM-DD): ").strip()
            try:
                room_id = int(room_id_str)
            except ValueError:
                print("ID de habitación inválido")
                continue
            start = parse_date(start_str)
            end = parse_date(end_str)
            if not start or not end:
                print("Fechas inválidas")
                continue
            try:
                res = manager.create_reservation(guest, room_id, start, end)
                print(f"Reserva creada con ID {res.reservation_id}. Total aprox: ${res.calculate_total_cost():.2f}")
            except Exception as e:
                print(f"Error: {e}")

        elif option == "4":
            reservations = manager.list_reservations()
            print("\nReservas:")
            for r in reservations:
                print(
                    f"- ID {r.reservation_id} | Huesped: {r.guest_name} | Hab: {r.room.id} | "
                    f"{r.check_in} -> {r.check_out} | Noches: {r.num_nights()} | Total: ${r.calculate_total_cost():.2f}"
                )
            if not reservations:
                print("(No hay reservas)")

        elif option == "5":
            res_id_str = input("ID de la reserva: ").strip()
            try:
                res_id = int(res_id_str)
            except ValueError:
                print("ID inválido")
                continue
            try:
                total = manager.calculate_reservation_cost(res_id)
                print(f"Costo total: ${total:.2f}")
            except Exception as e:
                print(f"Error: {e}")

        elif option == "6":
            res_id_str = input("ID de la reserva a cancelar: ").strip()
            try:
                res_id = int(res_id_str)
            except ValueError:
                print("ID inválido")
                continue
            ok = manager.cancel_reservation(res_id)
            print("Reserva cancelada" if ok else "Reserva no encontrada")

        elif option == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()


