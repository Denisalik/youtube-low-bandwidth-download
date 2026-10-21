from fastapi import APIRouter, BackgroundTasks, HTTPException
from sqlmodel import col, select

from src.db import SessionDep, download_file, file_delete_by_id
from src.entity.file import CreateFile, File

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=list[File])
def get_files(session: SessionDep):
    statement = select(File).order_by(col(File.id).desc())
    return session.exec(statement).all()


@router.get("/{file_id}")
def get_file(file_id: int, session: SessionDep):
    file = session.get(File, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.post("", response_model=File, status_code=201)
def create_file(create_file: CreateFile, session: SessionDep):
    file = File(url=create_file.url)
    if CreateFile.is_valid_format(create_file.format):
        file.format = create_file.format
    if CreateFile.is_valid_state(create_file.state):
        file.state = create_file.state
    session.add(file)
    session.commit()
    session.refresh(file)
    return file


@router.put("/{file_id}/download/{format}")
def download_file_in_format(
    file_id: int, format: str, session: SessionDep, background: BackgroundTasks
):
    file = session.get(File, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if not CreateFile.is_valid_format(format):
        raise HTTPException(status_code=400, detail="format can only be: 360, 720 or audio")
    file.state = "start"
    session.add(file)
    session.commit()
    background.add_task(download_file, file_id, format)
    return {"ok": True}


@router.delete("/{file_id}")
def delete_file(file_id: int, session: SessionDep):
    file_delete_by_id(file_id, session)
    return {"ok": True}
