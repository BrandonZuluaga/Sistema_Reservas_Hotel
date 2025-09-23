# Sistema de Reservas de Hotel (Consola + SQLAlchemy + Alembic)

Aplicación de consola en Python que gestiona reservas de hotel con persistencia en base de datos relacional (PostgreSQL/Neon) usando SQLAlchemy ORM y migraciones con Alembic. Incluye login de usuarios, auditoría y un menú interactivo.

## Características
- Modelado con SQLAlchemy ORM, claves primarias UUID y columnas de autoría.
- Migraciones con Alembic autogeneradas desde Base.metadata.
- Login de usuarios con hashing bcrypt (Passlib).
- Menú interactivo para listar habitaciones, disponibilidad, crear clientes y reservas, cancelar reservas.
- Estilo de código formateado con Black; solo se usan DocStrings.

## Estructura

/Users/josuaza/progra/
├── .gitignore
├── .venv/                       # entorno virtual (local)
├── requirements.txt
├── alembic.ini
├── migrations/
│   ├── env.py
│   ├── README
│   └── versions/
├── database/
│   ├── __init__.py
│   ├── base.py                  # Base declarativa, UUID y Audit mixins
│   ├── config.py                # carga DATABASE_URL
│   ├── session.py               # engine + SessionLocal
│   └── models/
│       ├── __init__.py
│       └── entities.py          # User, Role, Customer, RoomType, Room, Amenity, RoomAmenity, Reservation, Payment
├── hotel/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── room.py              # ejemplo OOP (no persistente)
│   │   └── reservation.py       # ejemplo OOP (no persistente)
│   └── services/
│       ├── __init__.py
│       ├── auth.py              # login y creación de usuarios
│       ├── booking_manager.py   # versión en memoria (legado)
│       └── booking_repository.py# capa ORM para reservas
└── main.py                      # CLI con login y operaciones sobre BD


## Requisitos
- Python 3.10+
- Cuenta PostgreSQL gestionada (p. ej. Neon)

## Instalación
bash
python3 -m venv /Users/josuaza/progra/.venv
source /Users/josuaza/progra/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r /Users/josuaza/progra/requirements.txt


## Configuración (.env)
Cree un archivo .env en la raíz con su URL de Neon (role/password/host/base):

DATABASE_URL=postgresql+psycopg://usuario:password@host:5432/base_de_datos
APP_DEBUG=true


## Migraciones (Alembic)
Inicializado con plantilla async y env.py lee DATABASE_URL del entorno.

- Generar migración inicial:
bash
source /Users/josuaza/progra/.venv/bin/activate
export DATABASE_URL=postgresql+psycopg://usuario:password@host:5432/base_de_datos
alembic revision --autogenerate -m "init schema"

- Aplicar migraciones:
bash
alembic upgrade head


## Uso
- Ejecutar el CLI:
bash
python /Users/josuaza/progra/main.py

- El sistema sembrará un usuario admin y tipos/habitaciones básicas.
- Inicie sesión con admin / admin123 (recomendado cambiar en BD luego).

### Menú
- Listar habitaciones
- Listar habitaciones disponibles por rango (YYYY-MM-DD)
- Crear cliente y reserva
- Listar reservas
- Cancelar reserva

## Entidades ORM
- User, Role, UserRole
- Customer
- RoomType
- Room, Amenity, RoomAmenity
- Reservation, Payment

Todas con id UUID y auditoría: id_usuario_creacion, id_usuario_edicion, fecha_creacion, fecha_actualizacion.

## Lógica de negocio
- Disponibilidad: se excluyen habitaciones con reservas activas que solapen el rango.
- Reservas: validación de fechas, estado confirmed/cancelled.
- Pagos: creación y asociación a reservas.

## Estilo de código
- Ejecutar Black para formatear:
bash