import logging
from pathlib import Path

from fastapi import HTTPException
from sqlmodel import Session, delete, select

from src.entity import File, FileState

from .engine import engine

logger = logging.getLogger(__name__)

FILES_DIR = Path("/data/files")


def file_delete_by_id(file_id: int, session: Session):
    file = session.get(File, id)
    if file is None or file.file_name is None:
        logger.error(f"Failed to delete id: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    file_path = FILES_DIR / file.file_name
    if not file_path.is_file():
        logger.error(f"Failed to delete path: {file_path}, it is not a file")
        raise HTTPException(status_code=404, detail="File not found")
    try:
        file_path.unlink()
        logger.info(f"Deleted file: {file_path}")
        session.delete(file)
        session.commit()
        logger.info(f"Deleted file in db, url: {file.url}")
    except OSError as e:
        logger.error(f"Failed to delete path: {file_path}, error: {e}")
        raise HTTPException(status_code=409, detail=f"Failed to delete {file_path}") from e


def file_cleanup_task():
    with Session(engine) as session:
        statement = select(File).where(
            (File.state == FileState.end)
            | (File.state == FileState.error)
            | (File.state == FileState.start)
        )
        files = session.exec(statement).all()
        for file in files:
            if file.file_name is None:
                logger.info(f"Deleted file with url: {file.url}")
                file.state = FileState.deleted
                continue
            file_path = FILES_DIR / file.file_name
            if file_path.is_file():
                try:
                    file_path.unlink()
                    file.state = FileState.deleted
                    logger.info(f"Deleted file: {file_path}")
                except OSError as e:
                    file.state = FileState.error
                    logger.error(f"Failed to delete {file_path}: {e}")
                    continue
            else:
                file.state = FileState.deleted
                logger.warning(f"File not found, skipping: {file_path}")
            session.add(file)
        session.commit()


def db_cleanup_task():
    with Session(engine) as session:
        statement = delete(File).where(
            (File.state == FileState.deleted) | (File.state == FileState.start)
        )
        session.exec(statement)
        session.commit()
