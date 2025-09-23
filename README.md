# Sistema de Reservas de Hotel (Consola)

Aplicación de consola en Python que gestiona reservas de hotel con tres tipos de habitaciones: estándar, suites y premium. Permite reservar, cancelar y calcular el costo total.

## Características
- Herencia y polimorfismo: `StandardRoom`, `SuiteRoom` y `PremiumRoom` heredan de `Room` y sobrescriben `calculate_price`.
- Encapsulamiento: acceso a atributos mediante propiedades.
- Operaciones: listar habitaciones, buscar disponibilidad, reservar, listar reservas, cancelar, calcular costos.

## Estructura
```
/Users/progra/
├── main.py
└── hotel/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   ├── room.py
    │   └── reservation.py
    └── services/
        ├── __init__.py
        └── booking_manager.py
```

## Requisitos
- Python 3.9+

## Ejecución
```bash
python /Users/progra/main.py
```

## Uso rápido
1. "Listar habitaciones" para ver todas las disponibles en el hotel.
2. "Listar habitaciones disponibles" ingresando rango de fechas (YYYY-MM-DD) y tipo (opcional: estandar/suite/premium).
3. "Crear reserva" ingresando nombre, id de habitación, check-in y check-out.
4. "Listar reservas" para ver las existentes y costos.
5. "Calcular costo de una reserva" proporcionando el ID.
6. "Cancelar reserva" por ID.

## Diseño OOP
- `Room` (abstracta): define interfaz y propiedades comunes.
- `StandardRoom`: costo lineal por noche.
- `SuiteRoom`: costo con recargo del 15%.
- `PremiumRoom`: costo con recargo del 30% + tarifa fija de concierge.
- `Reservation`: valida fechas, contiene cálculo de noches y total usando polimorfismo del `Room`.
- `BookingManager`: CRUD y validación de solapamientos.

### Ramificación
- rama principal: `main`
- rama secundarias: `main`, `prod`, `qa`, `dev`

## Licencia
Uso educativo.
