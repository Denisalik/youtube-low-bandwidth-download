from contextlib import asynccontextmanager

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.router import disk_router, file_router
from src.db import create_db_and_tables, file_cleanup_task, db_cleanup_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    create_db_and_tables()
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        file_cleanup_task,
        CronTrigger(hour=4, minute=0),
        id="file_cleanup"
    )
    scheduler.add_job(
        db_cleanup_task,
        CronTrigger(hour=3, minute=0),
        id="db_cleanup"
    )
    scheduler.start()
    yield
    # on exit
    scheduler.shutdown()

app = FastAPI(title='youtube-download-app', lifespan=lifespan)

app.include_router(file_router)
app.include_router(disk_router)
