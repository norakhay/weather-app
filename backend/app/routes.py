from flask import Blueprint, current_app, request

from app.city_service import CityService
from app.errors import require_city_name, success
from app.weather import WeatherService

api = Blueprint("api", __name__)
weather_service = WeatherService()
city_service = CityService()


@api.get("/api/health")
def health():
    return success({"status": "ok", "mock_weather": current_app.config.get("USE_MOCK_WEATHER", False)})


@api.get("/api/weather")
def get_weather():
    city = require_city_name(request.args.get("city"))
    return success(weather_service.get_current_weather(city).to_dict())


@api.get("/api/cities")
def list_cities():
    return success(city_service.list_cities())


@api.post("/api/cities")
def create_city():
    body = request.get_json(silent=True) or {}
    city = city_service.create_city(require_city_name(body.get("city_name")))
    return success(city, 201)


@api.get("/api/cities/<int:city_id>")
def get_city(city_id: int):
    return success(city_service.get_city(city_id))


@api.put("/api/cities/<int:city_id>")
def update_city(city_id: int):
    body = request.get_json(silent=True) or {}
    city = city_service.update_city(city_id, require_city_name(body.get("city_name")))
    return success(city)


@api.delete("/api/cities/<int:city_id>")
def delete_city(city_id: int):
    city_service.delete_city(city_id)
    return success({"deleted": True})
