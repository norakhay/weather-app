# API

Base URL when talking to Flask directly: `http://localhost:5000`.

From the Next.js UI, the same paths are used as `/api/...` and proxied to Flask.

## Envelope

Success:

```json
{ "success": true, "data": {} }
```

Error:

```json
{ "success": false, "error": "City not found" }
```

## Endpoints

### `GET /api/health`

Liveness check.

**Response `data`**

| Field | Type | Description |
| ----- | ---- | ----------- |
| `status` | string | `"ok"` |
| `mock_weather` | boolean | Whether the mock weather client is enabled |

### `GET /api/weather?city={name}`

Current weather for a city.

**Query**

| Name | Required | Rules |
| ---- | -------- | ----- |
| `city` | yes | Trimmed, length 2–100 |

**Response `data`**

| Field | Type | Description |
| ----- | ---- | ----------- |
| `city` | string | Canonical city name |
| `country` | string or null | Country code |
| `temperature` | number | Celsius |
| `condition` | string | Description (e.g. `clear sky`) |
| `humidity` | number | Percent |
| `wind_speed` | number | m/s |
| `icon` | string or null | OpenWeatherMap icon id |
| `icon_url` | string or null | Icon image URL |

**Errors**

| Status | When |
| ------ | ---- |
| 400 | Missing or invalid city name |
| 404 | City not found |
| 502 | Missing/invalid API key, or weather provider failure |

### `GET /api/cities`

List saved cities (newest first depends on repository order).

**Response `data`:** array of saved city objects.

### `POST /api/cities`

Save a city. Body:

```json
{ "city_name": "London" }
```

Weather is fetched first. The stored name is the official name from the weather client.

**Status:** `201` on success.

**Errors**

| Status | When |
| ------ | ---- |
| 400 | Invalid `city_name` |
| 404 | Weather client does not know the city |
| 409 | City already saved |

### `GET /api/cities/<id>`

One saved city.

**Errors:** `404` if the id does not exist.

### `PUT /api/cities/<id>`

Replace the saved city with another name. Body: `{ "city_name": "Amman" }`. Weather is fetched for the new name.

**Errors:** `400`, `404` (missing id or unknown weather city).

### `DELETE /api/cities/<id>`

Remove a saved city.

**Response `data`:** `{ "deleted": true }`

**Errors:** `404` if the id does not exist.

## Saved city object

```json
{
  "id": 1,
  "city_name": "London",
  "country": "GB",
  "created_at": "2026-09-09T12:00:00+00:00"
}
```

## Example curl

```bash
curl "http://localhost:5000/api/health"
curl "http://localhost:5000/api/weather?city=Amman"
curl -X POST http://localhost:5000/api/cities -H "Content-Type: application/json" -d "{\"city_name\":\"London\"}"
curl http://localhost:5000/api/cities
curl http://localhost:5000/api/cities/1
curl -X PUT http://localhost:5000/api/cities/1 -H "Content-Type: application/json" -d "{\"city_name\":\"Amman\"}"
curl -X DELETE http://localhost:5000/api/cities/1
```

A Postman collection is in `postman/Weather_API.postman_collection.json`.
