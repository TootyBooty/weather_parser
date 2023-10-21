from datetime import tzinfo

import pytz
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # database
    POSTGRES_URL: str = (
        "postgresql+asyncpg://postgres:postgres@postgresql:5432/weather_service"
    )
    SIMILARITY_PERCENT: float = 0.1  # between 0 and 1

    OPENWEATHERMAP_API_KEY: str
    BASE_OPENWEATHERMAP_URL: str = "http://api.openweathermap.org/data/2.5"
    WEATHER_OPENWEATHERMAP_URL: str = f"{BASE_OPENWEATHERMAP_URL}/weather"
    GROUP_OPENWEATHERMAP_URL: str = f"{BASE_OPENWEATHERMAP_URL}/group"

    # network
    REQUEST_TIMEOUT: int = 5

    # time
    TIMEZONE: tzinfo = pytz.timezone("Europe/Moscow")

    class Config:
        env_file = ".env"


Config = Settings()
