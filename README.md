# hotel-booking-service

## Local setup

Install dependencies:

```powershell
poetry install
```

Create local env file:

```powershell
Copy-Item .env.example .env
```

PostgreSQL settings are read from environment variables:

```text
POSTGRES_DB=hotel_booking_service
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
```

Run Django checks:

```powershell
.\.venv\Scripts\python.exe bookingservice\manage.py check
```

Apply migrations after PostgreSQL is running:

```powershell
.\.venv\Scripts\python.exe bookingservice\manage.py migrate
```
