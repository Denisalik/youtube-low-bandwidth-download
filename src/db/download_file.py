import logging

from sqlmodel import Session

from .engine import engine
from src.entity.file import File, FileState
from src.yout import download, make_format

logger = logging.getLogger(__name__)

def download_file(file_id: int, format: str):
    with Session(engine) as session:
        try:
            file = session.get(File, file_id)
            if file is None:
                #not possible from /api/files/{id}/download
                logger.error("item %s disappeared before job ran", file_id)
                raise Exception('No file in db')
            if format == '360':
                file.format = make_format(False, 360, False)
            elif format == '720':
                file.format = make_format(False, 720, True)
            elif format == 'audio':
                file.format = make_format(True)
            else:
                #not possible from /api/files/{id}/download
                logger.error('format is wrong format is: %s', format)
                raise Exception('Format is wrong')
            download(file)
            file.state = FileState.end
        except Exception:
            session.rollback()
            file.state = FileState.error
            logger.exception("download failed for item %s", file_id)
        finally:
            session.add(file)
            session.commit()