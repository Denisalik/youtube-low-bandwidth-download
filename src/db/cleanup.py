
import logging
from pathlib import Path

from sqlmodel import Session, select, delete

from src.entity import File, FileState
from .engine import engine


logger = logging.getLogger(__name__)

FILES_DIR = Path("/data/files")


def file_cleanup_task():
    with Session(engine) as session:
        statement = select(File).where(File.state == FileState.end | File.state == FileState.error)
        files = session.exec(statement).all()
        for file in files:
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
                file.state = FileState.error
                logger.warning(f"File not found, skipping: {file_path}")
            session.add(file)
        session.commit()

def db_cleanup_task():
    with Session(engine) as session:
        statement = delete(File).where(File.state == FileState.deleted)
        session.exec(statement)
        session.commit()