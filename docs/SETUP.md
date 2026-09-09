# Setup

## Prerequisites

- Docker and Docker Compose (recommended), or
- Python 3.12+, Node.js 22+, PostgreSQL 16, Redis 7
- Optional: an [OpenWeatherMap](https://openweathermap.org/api) API key

## Environment

From the project root:

```bash
copy .env.example .env
```

On macOS/Linux use `cp .env.example .env`.

| Variable | Purpose |
| -------- | ------- |
| `DATABASE_URL` | PostgreSQL URL |
| `WEATHER_API_KEY` | OpenWeatherMap key (ignored when mock weather is on) |
| `WEATHER_API_URL` | Weather HTTP endpoint |
| `REDIS_URL` | Redis |
| `CELERY_BROKER_URL` | Celery broker |
| `CELERY_RESULT_BACKEND` | Celery results |
| `USE_MOCK_WEATHER` | `true` uses Amman/London mock data |
| `FLASK_ENV` | Flask environment |
| `FRONTEND_ORIGIN` | CORS allowlist for Flask |
| `API_URL` | Flask base URL used by the Next.js `/api` rewrite |
| `NEXT_PUBLIC_APP_NAME` | Frontend display name |

Do not commit `.env`. `.gitignore` already excludes it.

For demos without a real API key, keep `USE_MOCK_WEATHER=true`. Mock weather only supports **Amman** and **London**.

## Docker (recommended)

```bash
copy .env.example .env
docker compose up --build
```

| App | URL |
| --- | --- |
| UI | http://localhost:3000 |
| API | http://localhost:5000 |

Stop with `Ctrl+C`, or `docker compose down`.

Compose overrides database and Redis URLs so containers talk to the `postgres` and `redis` services, not `localhost`.

## Local processes (without full Compose)

1. Start PostgreSQL and Redis, or only those services:

   ```bash
   docker compose up postgres redis
   ```

2. Backend:

   ```bash
   pip install -r backend/requirements.txt
   cd backend
   python run.py
   ```

3. Frontend:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Optional Celery worker (from `backend/`):

   ```bash
   celery -A app.celery_app.celery worker --loglevel=info
   ```

   On Windows, if the worker fails, add `--pool=solo`.

Set `.env` so `DATABASE_URL`, `REDIS_URL`, and `API_URL` use `localhost` ports (`5432`, `6379`, `5000`).
