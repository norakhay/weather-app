import pytest

from app.city_service import CityService
from app.errors import AppError
from app.models import SavedCity
from app.weather import MockWeatherClient, WeatherService


class InMemoryCityRepository:
    def __init__(self):
        self.cities = []
        self._next_id = 1

    def list_all(self):
        return list(reversed(self.cities))

    def get_by_id(self, city_id: int):
        for city in self.cities:
            if city.id == city_id:
                return city
        raise AppError("Saved city not found", 404)

    def find_by_name(self, city_name: str):
        lowered = city_name.lower()
        for city in self.cities:
            if city.city_name.lower() == lowered:
                return city
        return None

    def create(self, city_name: str, country: str | None):
        city = SavedCity(id=self._next_id, city_name=city_name, country=country)
        self._next_id += 1
        self.cities.append(city)
        return city

    def update(self, city, city_name: str, country: str | None):
        city.city_name = city_name
        city.country = country
        return city

    def delete(self, city):
        self.cities.remove(city)


def make_service():
    return CityService(
        repository=InMemoryCityRepository(),
        weather_service=WeatherService(client=MockWeatherClient()),
    )


def test_create_city_uses_canonical_weather_name():
    created = make_service().create_city("amman")
    assert created["city_name"] == "Amman"
    assert created["country"] == "JO"


def test_create_city_rejects_duplicates():
    service = make_service()
    service.create_city("London")
    with pytest.raises(AppError, match="already saved"):
        service.create_city("london")


def test_delete_city_removes_record():
    service = make_service()
    created = service.create_city("London")
    service.delete_city(created["id"])
    assert service.list_cities() == []
