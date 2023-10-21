from datetime import datetime

from core.config import Config
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(length=127), unique=True)

    weathers = relationship("Weather", back_populates="city")


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(
        String(length=127), ForeignKey("cities.city_name"), nullable=False
    )
    temperature = Column(Numeric(5, 2), nullable=False)
    atmospheric_pressure = Column(Numeric(6, 2), nullable=False)
    wind_speed = Column(Numeric(5, 2), nullable=False)
    measurement_date = Column(
        DateTime,
        default=lambda: datetime.now(Config.TIMEZONE).replace(
            tzinfo=None, microsecond=0
        ),
    )

    city = relationship("City", back_populates="weathers")
