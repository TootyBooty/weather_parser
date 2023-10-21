from db.models import City
from db.repositories.base import BaseRepository
from schemas.city import CityResponse
from sqlalchemy import select


class CityRepository(BaseRepository):
    async def get_city_ids(self) -> list[int]:
        async with self.session.begin():
            query = select(City.city_id)
            res = await self.session.execute(query)
            city_ids = [city[0] for city in res]
            return city_ids

    async def add_city(self, city: CityResponse):
        async with self.session.begin():
            new_city = City(city_id=city.city_id, city_name=city.city_name)
            self.session.add(new_city)
            return city
