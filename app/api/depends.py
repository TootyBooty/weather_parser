from aiohttp import ClientSession
from db.repositories.city import CityRepository
from db.repositories.weather import WeatherRepository
from db.session import get_session
from fastapi import Depends


async def get_weather_repository(session=Depends(get_session)) -> WeatherRepository:
    return WeatherRepository(session)


async def get_city_repository(session=Depends(get_session)) -> CityRepository:
    return CityRepository(session)


async def get_aiohttp_session() -> ClientSession:
    """Dependency for getting aiohttp session"""
    try:
        session = ClientSession()
        yield session
    finally:
        await session.close()
