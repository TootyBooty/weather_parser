import asyncio
from typing import List

from db.repositories.city import CityRepository
from db.repositories.weather import WeatherRepository
from db.session import async_session
from network.openweather import fetch_weather_data
from schemas.weather import WeatherCreate


async def get_weather_data_for_city_ids(city_ids: List[int]) -> List[WeatherCreate]:
    chunks = [city_ids[i : i + 20] for i in range(0, len(city_ids), 20)]
    results = await asyncio.gather(*(fetch_weather_data(chunk) for chunk in chunks))
    flattened_results = [item for sublist in results for item in sublist]
    return [WeatherCreate(**data) for data in flattened_results]


async def measurement_recording_task():
    async with async_session() as db_session:
        city_repo = CityRepository(session=db_session)
        weather_repo = WeatherRepository(session=db_session)

        city_ids = await city_repo.get_city_ids()
        weather_data = await get_weather_data_for_city_ids(city_ids)
        await weather_repo.add_measurements(measurements=weather_data)
