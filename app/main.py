import asyncio
from contextlib import asynccontextmanager

from api.routers import v1_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter
from fastapi import FastAPI
from scheduler.tasks import measurement_recording_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler(event_loop=asyncio.get_event_loop())
    scheduler.start()

    scheduler.add_job(measurement_recording_task, trigger=IntervalTrigger(minutes=1))

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


main_api_router = APIRouter()

main_api_router.include_router(v1_router)

app.include_router(main_api_router)
