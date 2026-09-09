import logging

from app.celery_app import celery
from app.config import Config
from app.weather import MockWeatherClient, OpenWeatherMapClient

logger = logging.getLogger(__name__)


@celery.task(name="log_saved_city_weather")
def log_saved_city_weather(city_name: str) -> dict:
    client = MockWeatherClient() if Config.USE_MOCK_WEATHER else OpenWeatherMapClient(
        Config.WEATHER_API_KEY,
        Config.WEATHER_API_URL,
    )
    weather = client.get_current_weather(city_name)
    logger.info("Saved city weather: %s %.1fC %s", weather.city, weather.temperature, weather.condition)
    return weather.to_dict()
