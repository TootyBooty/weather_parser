import logging
from decimal import Decimal
from decimal import ROUND_DOWN
from typing import Any
from typing import Dict
from typing import List

from aiohttp import ClientSession
from core.config import Config
from exceptions import NetworkException
from network.base import make_request
from schemas.city import CityResponse


async def fetch_weather_data(city_ids: List[int]) -> List[Dict[str, Any]]:
    async with ClientSession() as session:
        params = {
            "id": ",".join(map(str, city_ids)),
            "units": "metric",
            "appid": Config.OPENWEATHERMAP_API_KEY,
        }

        try:
            data = await make_request(
                session=session,
                url=Config.GROUP_OPENWEATHERMAP_URL,
                method="get",
                params=params,
            )

            weather_measurements = [
                {
                    "city_name": city["name"],
                    "temperature": Decimal(city["main"]["temp"]).quantize(
                        Decimal("0.00"), rounding=ROUND_DOWN
                    ),
                    "atmospheric_pressure": Decimal(city["main"]["pressure"]).quantize(
                        Decimal("0.00"), rounding=ROUND_DOWN
                    ),
                    "wind_speed": Decimal(city["wind"]["speed"]).quantize(
                        Decimal("0.00"), rounding=ROUND_DOWN
                    ),
                }
                for city in data["list"]
            ]
            logging.info(
                f"Информация о погоде успешно загружена.\nКоличество записей = {len(weather_measurements)}"
            )
            return weather_measurements

        except NetworkException as e:
            logging.warning(
                f"Произошла ошибка при получении информации о погоде.\nstatus code = {e.status_code}, detail = {e.detail}"
            )


async def check_city_info(city_name: str, session: ClientSession) -> CityResponse:
    params = {"q": city_name, "appid": Config.OPENWEATHERMAP_API_KEY}

    data = await make_request(
        session=session,
        url=Config.WEATHER_OPENWEATHERMAP_URL,
        method="get",
        params=params,
    )

    return CityResponse(
        city_id=data["id"],
        city_name=data["name"],
    )
