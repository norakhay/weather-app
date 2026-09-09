from dataclasses import asdict, dataclass

import requests
from flask import current_app

from app.errors import AppError

ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"


@dataclass(frozen=True)
class WeatherInfo:
    city: str
    country: str | None
    temperature: float
    condition: str
    humidity: int
    wind_speed: float
    icon: str | None
    icon_url: str | None

    def to_dict(self) -> dict:
        return asdict(self)


MOCK_CITIES = {
    "amman": WeatherInfo("Amman", "JO", 24.5, "clear sky", 40, 3.2, "01d", ICON_URL.format(icon="01d")),
    "london": WeatherInfo("London", "GB", 12.0, "light rain", 78, 5.1, "10d", ICON_URL.format(icon="10d")),
}


class MockWeatherClient:
    def get_current_weather(self, city: str) -> WeatherInfo:
        weather = MOCK_CITIES.get(city.strip().lower())
        if weather is None:
            raise AppError("City not found", 404)
        return weather


class OpenWeatherMapClient:
    def __init__(self, api_key: str, api_url: str):
        self.api_key = api_key
        self.api_url = api_url

    def get_current_weather(self, city: str) -> WeatherInfo:
        if not self.api_key:
            raise AppError("WEATHER_API_KEY is not configured", 502)
        try:
            response = requests.get(
                self.api_url,
                params={"q": city, "appid": self.api_key, "units": "metric"},
                timeout=8,
            )
        except requests.RequestException as exc:
            raise AppError("Could not reach the weather provider", 502) from exc

        if response.status_code == 404:
            raise AppError("City not found", 404)
        if response.status_code == 401:
            raise AppError("Invalid weather API key", 502)
        if not response.ok:
            raise AppError("Weather provider returned an error", 502)

        payload = response.json()
        weather = (payload.get("weather") or [{}])[0]
        icon = weather.get("icon")
        return WeatherInfo(
            city=payload.get("name") or city,
            country=(payload.get("sys") or {}).get("country"),
            temperature=payload.get("main", {}).get("temp"),
            condition=weather.get("description", "unknown"),
            humidity=payload.get("main", {}).get("humidity"),
            wind_speed=payload.get("wind", {}).get("speed"),
            icon=icon,
            icon_url=ICON_URL.format(icon=icon) if icon else None,
        )


class WeatherService:
    def __init__(self, client=None):
        self.client = client

    def get_current_weather(self, city: str) -> WeatherInfo:
        return self._client().get_current_weather(city)

    def _client(self):
        if self.client is not None:
            return self.client
        if current_app.config.get("USE_MOCK_WEATHER"):
            return MockWeatherClient()
        return OpenWeatherMapClient(
            current_app.config["WEATHER_API_KEY"],
            current_app.config["WEATHER_API_URL"],
        )
