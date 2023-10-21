from datetime import datetime
from decimal import Decimal
from decimal import ROUND_DOWN

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from typing_extensions import Annotated


class CustomModel(BaseModel):
    class Config:
        from_attributes = True


class WeatherCreate(CustomModel):
    city_name: Annotated[str, Field(min_length=1, max_length=127)]
    temperature: Annotated[Decimal, Field(max_digits=5, decimal_places=2)]
    atmospheric_pressure: Annotated[Decimal, Field(max_digits=6, decimal_places=2)]
    wind_speed: Annotated[Decimal, Field(max_digits=5, decimal_places=2)]

    @validator("city_name", pre=True, always=True)
    def remove_single_quote(cls, city_name: str) -> str:
        return city_name.replace("'", "")


class WeatherCurrentShow(WeatherCreate):
    pass


class WeatherShow(WeatherCurrentShow):
    measurement_date: datetime


class WeatherListWithAverages(CustomModel):
    avg_temperature: Decimal
    avg_atmospheric_pressure: Decimal
    avg_wind_speed: Decimal
    weather_measurements: list[WeatherShow]

    @validator(
        "avg_temperature", "avg_atmospheric_pressure", "avg_wind_speed", pre=True
    )
    def float_to_decimal_and_round(cls, value: float) -> Decimal:
        return Decimal(str(value)).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
