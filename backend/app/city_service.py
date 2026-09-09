from flask import current_app, has_app_context

from app.city_repository import CityRepository
from app.errors import AppError
from app.weather import WeatherService


class CityService:
    def __init__(self, repository=None, weather_service=None):
        self.repository = repository or CityRepository()
        self.weather_service = weather_service or WeatherService()

    def list_cities(self) -> list[dict]:
        return [city.to_dict() for city in self.repository.list_all()]

    def get_city(self, city_id: int) -> dict:
        return self.repository.get_by_id(city_id).to_dict()

    def create_city(self, city_name: str) -> dict:
        if self.repository.find_by_name(city_name):
            raise AppError("City is already saved", 409)
        weather = self.weather_service.get_current_weather(city_name)
        city = self.repository.create(weather.city, weather.country)
        self._queue_log(city.city_name)
        return city.to_dict()

    def update_city(self, city_id: int, city_name: str) -> dict:
        city = self.repository.get_by_id(city_id)
        weather = self.weather_service.get_current_weather(city_name)
        updated = self.repository.update(city, weather.city, weather.country)
        return updated.to_dict()

    def delete_city(self, city_id: int) -> None:
        self.repository.delete(self.repository.get_by_id(city_id))

    def _queue_log(self, city_name: str) -> None:
        if has_app_context() and current_app.config.get("TESTING"):
            return
        try:
            from app.tasks import log_saved_city_weather

            log_saved_city_weather.delay(city_name)
        except Exception:
            pass
