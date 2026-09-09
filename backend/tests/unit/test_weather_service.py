import pytest

from app.errors import AppError
from app.weather import MockWeatherClient, WeatherService


class FakeFailingClient:
    def get_current_weather(self, city: str):
        raise AppError("down", 502)


def test_mock_client_returns_known_city():
    weather = MockWeatherClient().get_current_weather("Amman")
    assert weather.city == "Amman"
    assert weather.temperature == 24.5


def test_mock_client_rejects_unknown_city():
    with pytest.raises(AppError, match="City not found"):
        MockWeatherClient().get_current_weather("Atlantis")


def test_weather_service_uses_injected_client():
    weather = WeatherService(client=MockWeatherClient()).get_current_weather("London")
    assert weather.condition == "light rain"


def test_weather_service_propagates_provider_errors():
    with pytest.raises(AppError):
        WeatherService(client=FakeFailingClient()).get_current_weather("Amman")
