from api.v1.routers import weather_router
from fastapi import APIRouter


v1_router = APIRouter(prefix="/api/v1", tags=["v1"])

v1_router.include_router(weather_router, prefix="/weather")
