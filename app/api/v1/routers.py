from datetime import datetime
from typing import Annotated

import exceptions as exc
from aiohttp import ClientSession
from api.depends import get_aiohttp_session
from api.depends import get_city_repository
from api.depends import get_weather_repository
from db.repositories.city import CityRepository
from db.repositories.weather import WeatherRepository
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from network.base import NetworkException
from network.openweather import check_city_info
from schemas.weather import WeatherCurrentShow
from schemas.weather import WeatherListWithAverages
from schemas.weather import WeatherShow
from sqlalchemy.exc import IntegrityError


weather_router = APIRouter()


@weather_router.post("/{city}/")
async def add_city(
    city: str = Path(min_length=1, max_length=127),
    city_repo: CityRepository = Depends(get_city_repository),
    aiohttp_session: ClientSession = Depends(get_aiohttp_session),
):
    async with aiohttp_session as session:
        try:
            city_info = await check_city_info(city_name=city, session=session)
        except NetworkException:
            raise exc.CityNotFound

        try:
            return await city_repo.add_city(city=city_info)
        except IntegrityError:
            raise exc.CityAlreadyExists


@weather_router.get("/")
async def get_current_weather(
    weather_repo: WeatherRepository = Depends(get_weather_repository),
    search: Annotated[str | None, Query(max_length=127)] = None,
):
    weather_measurements = await weather_repo.get_current_weather(search=search)
    if not weather_measurements:
        raise exc.EmptyCitySearch
    return [
        WeatherCurrentShow.model_validate(weather) for weather in weather_measurements
    ]


@weather_router.get("/detail/")
async def get_detailed_weather_for_period(
    weather_repo: WeatherRepository = Depends(get_weather_repository),
    city: str = Query(min_length=1, max_length=127),
    start_date: Annotated[
        datetime,
        Query(
            description="YYYY-MM-DDTHH:MM:SS",
            example="2023-10-23T19:56:20",
            ge=datetime(2000, 1, 1),
            le=datetime(2100, 1, 1),
        ),
    ] = None,
    end_date: Annotated[
        datetime,
        Query(
            description="YYYY-MM-DDTHH:MM:SS",
            example="2023-10-23T19:56:20",
            ge=datetime(2000, 1, 1),
            le=datetime(2100, 1, 1),
        ),
    ] = None,
    limit: int = Query(ge=1, le=5000, default=5000),
):

    city = city.capitalize()
    weather_measurements, averages = await weather_repo.get_city_weather_and_averages(
        city,
        limit,
        start_date,
        end_date,
    )

    if not weather_measurements or not averages:
        raise exc.CityOrMeasurementsNotExists

    return WeatherListWithAverages(
        avg_temperature=averages["avg_temperature"],
        avg_atmospheric_pressure=averages["avg_atmospheric_pressure"],
        avg_wind_speed=averages["avg_wind_speed"],
        weather_measurements=[
            WeatherShow.model_validate(weather) for weather in weather_measurements
        ],
    )
