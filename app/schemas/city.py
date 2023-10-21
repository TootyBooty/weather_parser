from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from typing_extensions import Annotated


class CityResponse(BaseModel):
    city_id: Annotated[int, Field(gt=0)]
    city_name: Annotated[str, Field(min_length=1, max_length=127)]

    @validator("city_name", pre=True, always=True)
    def remove_single_quote(cls, city_name: str) -> str:
        return city_name.replace("’", "").replace("'", "")


class CityCreate(CityResponse):
    pass
