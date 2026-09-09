# Architecture

This document describes how the weather app is structured and why each layer exists.

## Overview

The product is a small full-stack app: search a city, show current weather, and save or remove favorite cities.

```text
Browser (Next.js UI on :3000)
        │
        │  fetch("/api/...")
        ▼
Next.js rewrite  →  Flask API on :5000
        │
        ├── WeatherService → OpenWeatherMap or mock
        └── CityService
                ├── CityRepository → PostgreSQL (`saved_cities`)
                └── (after save) Celery task via Redis
```

There is no authentication. The UI and API are intended to run together locally or with Docker Compose.

## Backend layers

| Layer | Files | Responsibility |
| ----- | ----- | -------------- |
| HTTP | `backend/app/routes.py` | Parse requests, call services, return JSON |
| Errors | `backend/app/errors.py` | Shared `{ success, data }` / `{ success, error }` shape |
| Services | `backend/app/city_service.py`, `weather.py` | Business rules |
| Persistence | `backend/app/city_repository.py`, `models.py` | SQLAlchemy queries and the `SavedCity` model |
| Background | `backend/app/tasks.py`, `celery_app.py` | Log weather after a city is saved |

Routes do not query the database or call OpenWeatherMap directly. That keeps HTTP handlers thin and makes unit tests possible without Flask or PostgreSQL.

### Weather clients

`WeatherService` picks a client from config:

- **Mock** (`USE_MOCK_WEATHER=true`): in-memory data for **Amman** and **London**. Any other city returns `404 City not found`.
- **OpenWeatherMap**: live current weather (`units=metric`). Official city name and country code come from the provider response.

Saving a city always goes through the weather client first. The stored `city_name` is the provider’s canonical name, not whatever the user typed.

### City save flow

1. Reject empty or invalid names (2–100 characters).
2. Reject duplicates (`409 City is already saved`).
3. Fetch weather so the city is known to exist.
4. Insert into `saved_cities`.
5. Queue `log_saved_city_weather` on Celery. If Redis is down, the insert still succeeds. Tests skip the queue (`TESTING=true`).

## Frontend

| Path | Role |
| ---- | ---- |
| `frontend/app/page.tsx` | Screen state: search, save, delete, load favorites |
| `frontend/services/api.ts` | Typed `fetch` helpers against `/api/*` |
| `frontend/components/` | Search bar, weather card, saved list, loading and error UI |
| `frontend/next.config.ts` | Rewrites `/api/:path*` to Flask (`API_URL`) |

The browser never talks to port 5000 in development. Same-origin `/api` calls avoid CORS issues in the UI. Flask still enables CORS for `FRONTEND_ORIGIN` so Postman or other clients can call the API directly.

## Data

One table: `saved_cities`.

| Column | Type | Notes |
| ------ | ---- | ----- |
| `id` | integer PK | Auto-increment |
| `city_name` | string, unique | Canonical name from weather data |
| `country` | string, nullable | ISO country code from weather data |
| `created_at` | timestamptz | UTC |

Tables are created with `db.create_all()` when the Flask app starts. There is no separate migration tool.

## Docker Compose services

| Service | Image / build | Port |
| ------- | ------------- | ---- |
| `postgres` | postgres:16-alpine | 5432 |
| `redis` | redis:7-alpine | 6379 |
| `backend` | `backend/Dockerfile` (Gunicorn) | 5000 |
| `celery` | same backend image, worker command | — |
| `frontend` | `frontend/Dockerfile` (Next.js production) | 3000 |

Inside Compose, the frontend build arg `API_URL=http://backend:5000` so rewrites target the backend container, not localhost.
