from datetime import datetime
from typing import Optional

from db.models import Weather
from db.repositories.base import BaseRepository
from schemas.weather import WeatherCreate
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import select


class WeatherRepository(BaseRepository):
    async def add_measurements(self, measurements: list[WeatherCreate]) -> int:
        async with self.session.begin():
            new_measurements = [
                Weather(
                    city_name=measurement.city_name,
                    temperature=measurement.temperature,
                    atmospheric_pressure=measurement.atmospheric_pressure,
                    wind_speed=measurement.wind_speed,
                )
                for measurement in measurements
            ]
            self.session.add_all(new_measurements)
            return len(new_measurements)

    async def get_current_weather(self, search: Optional[str] = None) -> list[Weather]:
        async with self.session.begin():
            # Создаем подзапрос для LatestWeather
            subquery = select(
                Weather.city_name,
                func.max(Weather.measurement_date).label("latest_date"),
            ).group_by(Weather.city_name)

            if search:
                subquery = subquery.where(
                    func.similarity(Weather.city_name, search) >= 0.1
                )

            subquery = subquery.alias("lw")

            # Создаем основной запрос
            query = select(Weather).join(
                subquery,
                and_(
                    Weather.city_name == subquery.c.city_name,
                    Weather.measurement_date == subquery.c.latest_date,
                ),
            )

            # Выполняем запрос
            res = await self.session.execute(query)
            weather_measurements = res.scalars().all()
            if weather_measurements:
                return weather_measurements

    async def get_city_weather_and_averages(
        self,
        city: str,
        limit: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> tuple[list[Weather], dict[str, float]]:

        conditions = [Weather.city_name == city]

        if start_date:
            conditions.append(Weather.measurement_date >= start_date)
        if end_date:
            conditions.append(Weather.measurement_date <= end_date)

        query = (
            select(
                Weather,
                func.avg(Weather.temperature)
                .over(partition_by=Weather.city_name)
                .label("avg_temperature"),
                func.avg(Weather.atmospheric_pressure)
                .over(partition_by=Weather.city_name)
                .label("avg_atmospheric_pressure"),
                func.avg(Weather.wind_speed)
                .over(partition_by=Weather.city_name)
                .label("avg_wind_speed"),
            )
            .where(and_(*conditions))
            .limit(limit)
        )

        res = await self.session.execute(query)
        raw_data = res.all()

        if raw_data:
            # Извлекаем объекты Weather и средние значения
            weather_measurements = [row[0] for row in raw_data]
            averages = {
                "avg_temperature": raw_data[0][1],
                "avg_atmospheric_pressure": raw_data[0][2],
                "avg_wind_speed": raw_data[0][3],
            }

            return weather_measurements, averages
        return [], {}
