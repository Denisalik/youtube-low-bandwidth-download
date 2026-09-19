from fastapi import APIRouter, HTTPException, BackgroundTasks, HTTPException
from sqlmodel import select

from src.db import SessionDep, download_file
from src.entity.file import File, CreateFile


router = APIRouter(
    prefix="/api/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)

@router.get('', response_model=list[File])
def get_files(session: SessionDep):
    return session.exec(select(File)).all()

@router.get('/{id}')
def get_file(id: int, session: SessionDep):
    file = session.get(File, id)
    if not file:
        raise HTTPException(status_code=404, detail='File not found')
    return file

@router.post('', response_model=File, status_code=201)
def create_file(create_file: CreateFile, session: SessionDep):
    file = File(url=create_file.url)
    if CreateFile.is_valid_format(create_file.format):
        file.format = create_file.format
    session.add(file)
    session.commit()
    session.refresh(file)
    return file

@router.put('/{id}/download/{format}')
def download_file_in_format(id: int, format: str, session: SessionDep, background: BackgroundTasks):
    file = session.get(File, id)
    if not file:
        raise HTTPException(status_code=404, detail='File not found')
    if not CreateFile.is_valid_format(format):
        raise HTTPException(status_code=400, detail='format can only be: 360, 720 or audio')
    file.state = 'start'
    session.add(file)
    session.commit()
    background.add_task(download_file, id, format)
    return {'ok': True}

@router.delete('/{id}')
def delete_file(id: int, session: SessionDep):
    file = session.get(File, id)
    if not file:
        raise HTTPException(status_code=404, detail='File not found')
    session.delete(file)
    session.commit()
    return {'ok': True}