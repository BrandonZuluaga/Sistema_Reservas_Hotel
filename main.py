from __future__ import annotations

import os
import uuid
from datetime import date
from typing import Optional

from dotenv import load_dotenv
from rich import print

from database.session import SessionLocal
from database.base import Base
from database.models import User, Role, RoomType, Room
from hotel.services.auth import authenticate_user, create_user
from hotel.services.booking_repository import BookingRepository


load_dotenv()


def parse_date(input_str: str) -> Optional[date]:
    try:
        y, m, d = map(int, input_str.split("-"))
        return date(y, m, d)
    except Exception:
        return None


def ensure_seed_data(session) -> None:
    admin_role = session.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin", id_usuario_creacion=uuid.uuid4())
        session.add(admin_role)
        session.commit()
    admin_user = session.query(User).filter_by(username="admin").first()
    if not admin_user:
        create_user(
            session,
            username="admin",
            email="admin@example.com",
            password="admin123",
            actor_id=uuid.uuid4(),
        )
    rt_standard = session.query(RoomType).filter_by(name="estandar").first()
    if not rt_standard:
        rt_standard = RoomType(
            name="estandar",
            description="Habitación estándar",
            base_rate=100.0,
            id_usuario_creacion=uuid.uuid4(),
        )
        session.add(rt_standard)
        session.commit()
    any_room = session.query(Room).first()
    if not any_room:
        rooms = [
            Room(
                number="101",
                floor=1,
                capacity=2,
                status="available",
                room_type_id=rt_standard.id,
                id_usuario_creacion=uuid.uuid4(),
            ),
            Room(
                number="102",
                floor=1,
                capacity=2,
                status="available",
                room_type_id=rt_standard.id,
                id_usuario_creacion=uuid.uuid4(),
            ),
            Room(
                number="201",
                floor=2,
                capacity=3,
                status="available",
                room_type_id=rt_standard.id,
                id_usuario_creacion=uuid.uuid4(),
            ),
        ]
        session.add_all(rooms)
        session.commit()


def show_main_menu() -> None:
    print("\n[bold cyan]=== Sistema de Reservas de Hotel ===[/bold cyan]")
    print("1. Listar habitaciones")
    print("2. Listar habitaciones disponibles por rango")
    print("3. Crear cliente y reserva")
    print("4. Listar reservas")
    print("5. Cancelar reserva")
    print("0. Salir")


def login_flow(session) -> Optional[User]:
    print("\n[bold]Login[/bold]")
    username = input("Usuario: ").strip()
    password = input("Contraseña: ").strip()
    user = authenticate_user(session, username=username, password=password)
    if not user:
        print("[red]Credenciales inválidas[/red]")
        return None
    print(f"[green]Bienvenido {user.username}[/green]")
    return user


def main() -> None:
    with SessionLocal() as session:
        ensure_seed_data(session)
        print("\nConfigurar variable DATABASE_URL en .env para usar su Neon.")
        user = None
        while not user:
            user = login_flow(session)
            if not user:
                retry = input("¿Reintentar? (s/n): ").strip().lower()
                if retry != "s":
                    return

        repo = BookingRepository(session)

        while True:
            show_main_menu()
            option = input("Seleccione una opción: ").strip()

            if option == "1":
                rooms = repo.list_rooms()
                print("\nHabitaciones:")
                for r in rooms:
                    print(f"- {r.number} | Piso {r.floor} | Capacidad {r.capacity}")

            elif option == "2":
                start_str = input("Fecha inicio (YYYY-MM-DD): ").strip()
                end_str = input("Fecha fin (YYYY-MM-DD): ").strip()
                start = parse_date(start_str)
                end = parse_date(end_str)
                if not start or not end or end <= start:
                    print("[red]Fechas inválidas[/red]")
                    continue
                available = repo.list_available_rooms(start, end)
                print("\nDisponibles:")
                for r in available:
                    print(f"- {r.number} | Piso {r.floor} | Capacidad {r.capacity}")
                if not available:
                    print("(No hay habitaciones disponibles)")

            elif option == "3":
                full_name = input("Nombre completo del cliente: ").strip()
                document_id = input("Documento: ").strip()
                room_number = input("Número de habitación: ").strip()
                start_str = input("Check-in (YYYY-MM-DD): ").strip()
                end_str = input("Check-out (YYYY-MM-DD): ").strip()
                start = parse_date(start_str)
                end = parse_date(end_str)
                if not start or not end or end <= start:
                    print("[red]Fechas inválidas[/red]")
                    continue
                room = session.query(Room).filter_by(number=room_number).first()
                if not room:
                    print("[red]Habitación no encontrada[/red]")
                    continue
                customer = repo.create_customer(
                    full_name=full_name,
                    document_id=document_id,
                    actor_id=user.id,
                )
                reservation = repo.create_reservation(
                    customer_id=customer.id,
                    room_id=room.id,
                    check_in=start,
                    check_out=end,
                    actor_id=user.id,
                )
                print(f"[green]Reserva creada {reservation.id}[/green]")

            elif option == "4":
                reservations = repo.list_reservations()
                print("\nReservas:")
                for r in reservations:
                    print(
                        f"- {r.id} | Hab: {r.room_id} | {r.check_in} -> {r.check_out} | Estado: {r.status}"
                    )
                if not reservations:
                    print("(No hay reservas)")

            elif option == "5":
                res_id = input("ID de la reserva a cancelar: ").strip()
                try:
                    res_uuid = uuid.UUID(res_id)
                except Exception:
                    print("[red]ID inválido[/red]")
                    continue
                ok = repo.cancel_reservation(res_uuid, user.id)
                print(
                    "[green]Reserva cancelada[/green]"
                    if ok
                    else "[red]Reserva no encontrada[/red]"
                )

            elif option == "0":
                print("Saliendo...")
                break
            else:
                print("Opción no válida")


if __name__ == "_main_":
    main()