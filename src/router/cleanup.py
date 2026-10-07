from fastapi import APIRouter

from src.db import db_cleanup_task, file_cleanup_task

router = APIRouter(
    prefix="/api/cleanup",
    tags=["cleanup"],
)


@router.post("/file", response_model=str)
def cleanup_file_route():
    file_cleanup_task()
    return "Unused files starting to delete"


@router.post("/db", response_model=str)
def cleanup_db_route():
    db_cleanup_task()
    return "Unused db rows starting to delete"
