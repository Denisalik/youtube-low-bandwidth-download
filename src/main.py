from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.router import disk_router, file_router
from src.db import create_db_and_tables, file_cleanup_task, db_cleanup_task


file_cleanup_hour: int = int(os.getenv("FILE_CLEANUP_HOUR", "1"))
db_cleanup_hour: int = int(os.getenv("DB_CLEANUP_HOUR", "0"))
cleanup_minute: int = int(os.getenv("CLEANUP_MINUTE", "0"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    create_db_and_tables()
    
    scheduler = AsyncIOScheduler()
    #time is used is UTC, to get MSC time you need to add +3
    scheduler.add_job(
        file_cleanup_task,
        CronTrigger(hour=file_cleanup_hour, minute=cleanup_minute),
        id="file_cleanup"
    )
    scheduler.add_job(
        db_cleanup_task,
        CronTrigger(hour=db_cleanup_hour, minute=cleanup_minute),
        id="db_cleanup"
    )
    scheduler.start()
    yield
    # on exit
    scheduler.shutdown()

app = FastAPI(title='youtube-download-app', lifespan=lifespan)

app.include_router(file_router)
app.include_router(disk_router)
