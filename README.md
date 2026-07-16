# hotel-booking-service

Simple HTTP JSON API for managing hotel rooms and room bookings.

## Stack

- Python 3.14
- Django 5.2
- PostgreSQL 17
- Docker Compose
- Poetry

## Run Locally

Install dependencies:

```powershell
poetry install
```

Start PostgreSQL:

```powershell
docker compose up -d
```

Apply migrations:

```powershell
.\.venv\Scripts\python.exe .\bookingservice\manage.py migrate
```

Run the service on port `9000`:

```powershell
.\.venv\Scripts\python.exe .\bookingservice\manage.py runserver 9000
```

Run tests:

```powershell
.\.venv\Scripts\python.exe .\bookingservice\manage.py test hotels --noinput
```

## Database Schema

The application uses Django migrations during normal startup.

For review and manual database setup, the SQL schema is documented in:

```text
schema.sql
```

It contains table definitions for hotel rooms and bookings plus indexes used by booking lookups.

## Configuration

PostgreSQL settings are read from environment variables. Local defaults match `docker-compose.yml`.

```text
POSTGRES_DB=hotel_booking_service
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
```

To override them locally, copy the example env file and edit values:

```powershell
Copy-Item .env.example .env
```

## API

All successful responses return JSON. Error responses return JSON in this format:

```json
{"error": "error text"}
```

### Create Room

```text
POST /rooms/create
```

Input:

```text
description=Sea view room
price_per_night=5000.00
```

Example:

```powershell
curl.exe -X POST -d "description=Sea view room" -d "price_per_night=5000.00" http://127.0.0.1:9000/rooms/create
```

Response:

```json
{"room_id": 1}
```

### Delete Room

Deletes the room and its bookings.

```text
POST /rooms/delete
```

Example:

```powershell
curl.exe -X POST -d "room_id=1" http://127.0.0.1:9000/rooms/delete
```

Response:

```json
{"deleted": true}
```

### List Rooms

```text
GET /rooms/list
```

Optional query params:

```text
sort_by=price|created_at
order=asc|desc
```

Example:

```powershell
curl.exe "http://127.0.0.1:9000/rooms/list?sort_by=price&order=desc"
```

Response:

```json
[
  {
    "room_id": 1,
    "description": "Sea view room",
    "price_per_night": "5000.00",
    "created_at": "2026-07-16T19:46:27.885116+00:00"
  }
]
```

### Create Booking

```text
POST /bookings/create
```

Input:

```text
room_id=1
date_start=2026-07-20
date_end=2026-07-25
```

Example:

```powershell
curl.exe -X POST -d "room_id=1" -d "date_start=2026-07-20" -d "date_end=2026-07-25" http://127.0.0.1:9000/bookings/create
```

Response:

```json
{"booking_id": 1}
```

### Delete Booking

```text
POST /bookings/delete
```

Example:

```powershell
curl.exe -X POST -d "booking_id=1" http://127.0.0.1:9000/bookings/delete
```

Response:

```json
{"deleted": true}
```

### List Room Bookings

Bookings are sorted by `date_start`.

```text
GET /bookings/list?room_id=1
```

Example:

```powershell
curl.exe "http://127.0.0.1:9000/bookings/list?room_id=1"
```

Response:

```json
[
  {
    "booking_id": 1,
    "date_start": "2026-07-20",
    "date_end": "2026-07-25"
  }
]
```

## Decisions

- API is implemented with plain Django views and `JsonResponse`, without Django REST Framework.
- PostgreSQL runs in Docker on host port `5433` because local port `5432` may already be used by a system PostgreSQL installation.
- Dates use `YYYY-MM-DD`.
- `date_end` must be after `date_start`.
- Overlapping bookings for the same room are rejected.
- Adjacent bookings are allowed: an existing `2026-07-20` to `2026-07-25` booking allows a new booking starting on `2026-07-25`.
