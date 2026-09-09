# Testing

Run commands from the **project root** unless noted.

Install backend test dependencies (includes pytest and Playwright):

```bash
pip install -r backend/requirements.txt
playwright install chromium
```

`pytest.ini` sets `pythonpath = backend` and default `testpaths = backend/tests`.

## Unit tests

Location: `backend/tests/unit/`

- Weather client and service behavior
- City save/list/delete rules
- Request validation / schemas

These tests do not call OpenWeatherMap or PostgreSQL. Weather is mocked; city storage is in memory.

```bash
pytest backend/tests/unit
```

## Integration tests

Location: `backend/tests/integration/`

Flask test client + in-memory SQLite. Requests still go routes → services → database. Mock weather is enabled in fixtures (`conftest.py`). Celery is not used (`TESTING`).

```bash
pytest backend/tests/integration
```

All backend tests:

```bash
pytest backend/tests
```

## End-to-end tests

Location: `e2e/test_weather_flows.py`

Playwright drives the UI at `BASE_URL` (default `http://localhost:3000`).

Covered flows:

- Search Amman and see temperature
- Save London
- Save then delete Amman
- Unknown city (`Atlantis`) shows `City not found`

The API and UI must already be running. Use `USE_MOCK_WEATHER=true` so results are stable.

```bash
pytest e2e
```

Override the UI URL if needed:

```bash
set BASE_URL=http://localhost:3000
pytest e2e
```

On macOS/Linux: `BASE_URL=http://localhost:3000 pytest e2e`.
