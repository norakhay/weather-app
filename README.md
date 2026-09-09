# Weather App

Internship final project: a simple full-stack weather app. Search a city, view current weather, and save or remove favorite cities.

The app is intentionally small. Layers stay separate so routes do not contain business logic or database queries.

More detail:

- [Architecture](docs/ARCHITECTURE.md)
- [API](docs/API.md)
- [Setup](docs/SETUP.md)
- [Testing](docs/TESTING.md)

## Technologies

- **Backend:** Python, Flask, SQLAlchemy, PostgreSQL, Redis, Celery
- **Frontend:** React, Next.js, TypeScript
- **Weather data:** OpenWeatherMap (replaceable mock for tests)
- **Tests:** pytest (unit + integration), Playwright (E2E)
- **Ops:** Docker Compose

## Architecture

```text
Browser (Next.js UI)
        ↓  /api/*  (Next.js reverse proxy)
Flask routes
        ↓
Services (business rules)
        ├── WeatherClient → OpenWeatherMap or mock
        └── CityRepository → PostgreSQL
                ↓ (after save, optional)
        Celery task → Redis broker → worker logs weather
```

**Why this split**

- Routes only parse HTTP and return JSON.
- Services own rules such as “do not save a city twice” and “resolve the official city name from weather data”.
- Repositories own SQLAlchemy queries.
- The weather module can be swapped for a mock so tests do not call the internet.
- Celery is a side effect after save. If Redis is down, the city is still saved.

## Folder structure

```text
backend/app/
  routes.py           HTTP endpoints
  city_service.py     save/list/delete rules
  city_repository.py  database access
  weather.py          OpenWeatherMap + mock
  tasks.py            Celery background log
frontend/
  app/page.tsx        screen logic
  components/         UI pieces
  services/api.ts     calls Flask
```

## Database

One table, `saved_cities`:

| Column     | Purpose                          |
| ---------- | -------------------------------- |
| id         | Primary key                      |
| city_name  | Unique saved city                |
| country    | Country code from weather data   |
| created_at | When it was saved                |

No extra tables. There is no authentication.

## API endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/health` | Service check |
| GET | `/api/weather?city=Amman` | Current weather |
| GET | `/api/cities` | List saved cities |
| POST | `/api/cities` | Save a city `{ "city_name": "London" }` |
| GET | `/api/cities/<id>` | One saved city |
| PUT | `/api/cities/<id>` | Rename/update a saved city |
| DELETE | `/api/cities/<id>` | Remove a saved city |

Success:

```json
{ "success": true, "data": {} }
```

Error:

```json
{ "success": false, "error": "City not found" }
```

## Environment variables

Copy the example file and fill in values:

```bash
copy .env.example .env
```

| Variable | Used for |
| -------- | -------- |
| `DATABASE_URL` | PostgreSQL connection |
| `WEATHER_API_KEY` | OpenWeatherMap key |
| `WEATHER_API_URL` | Weather endpoint (default OpenWeatherMap) |
| `REDIS_URL` | Redis |
| `CELERY_BROKER_URL` | Celery queue |
| `CELERY_RESULT_BACKEND` | Celery results |
| `USE_MOCK_WEATHER` | `true` skips the real weather API |
| `API_URL` | Flask URL used by the Next.js `/api` proxy |
| `FRONTEND_ORIGIN` | CORS origin for the Flask app |

Never commit a real `.env` file.

For local demos without an API key, set `USE_MOCK_WEATHER=true`. Mock data exists for **Amman** and **London**. Any other city returns “City not found”.

## Docker (recommended)

```bash
copy .env.example .env
docker compose up --build
```

- UI: http://localhost:3000
- API: http://localhost:5000
- Postman: import `postman/Weather_API.postman_collection.json`

## Local setup (without full Docker)

1. Start PostgreSQL and Redis (or `docker compose up postgres redis`).
2. Create a virtualenv, then:

```bash
pip install -r backend/requirements.txt
cd backend
python run.py
```

3. In another terminal:

```bash
cd frontend
npm install
npm run dev
```

4. Optional Celery worker (from `backend/`):

```bash
celery -A app.celery_app.celery worker --loglevel=info
```

On Windows, if the worker fails to start, use `--pool=solo`.

## Redis and Celery

When a city is saved, Flask queues `log_saved_city_weather`. The worker fetches that city’s weather and writes a log line.

The HTTP response does not wait for the worker. Tests disable this queue. If Redis is unavailable, save still succeeds.

## Tests

From the project root:

```bash
pip install -r backend/requirements.txt
playwright install chromium
pytest backend/tests
```

Unit tests mock the weather provider and keep city logic in memory.

Integration tests use Flask’s test client and an in-memory SQLite database. They still go through routes → services → database.

E2E tests need the UI and API running (`USE_MOCK_WEATHER=true` recommended):

```bash
pytest e2e
```

## Example API requests

```bash
curl "http://localhost:5000/api/weather?city=Amman"
curl -X POST http://localhost:5000/api/cities -H "Content-Type: application/json" -d "{\"city_name\":\"London\"}"
curl http://localhost:5000/api/cities
curl -X DELETE http://localhost:5000/api/cities/1
```
