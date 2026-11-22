import os

from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, HTTPException

from src.ai import ELClient, ORClient
from src.db import SessionDep
from src.entity.file import File, FileState

load_dotenv()
or_api_key = os.getenv("OPEN_ROUTER_API_KEY")
if or_api_key is None:
    raise Exception("OPEN_ROUTER_API_KEY env variable is empty")

or_url = os.getenv("OPEN_ROUTER_URL")
if or_url is None:
    raise Exception("OPEN_ROUTER_URL env variable is empty")

el_api_key = os.getenv("ELEVEN_LABS_API_KEY")
if el_api_key is None:
    raise Exception("ELEVEN_LABS_API_KEY env variable is empty")

or_client = ORClient(or_api_key, or_url)
el_client = ELClient(el_api_key)


router = APIRouter(
    prefix="/api/ai",
    tags=["ai"],
    responses={
        400: {"description": "Format can only be: audio"},
        404: {"description": "Not found"},
    },
)


@router.post("/{file_id}")
def download_text(file_id: int, session: SessionDep, background: BackgroundTasks):
    file = session.get(File, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    if not file.state == FileState.end:
        raise HTTPException(status_code=400, detail="State can only be: end")
    if file.file_name is None:
        raise HTTPException(status_code=400, detail="file_name cannot be None")
    if file.format is None or "audio only" not in file.format or "+" in file.format:
        raise HTTPException(status_code=400, detail="Format can only be in audio only format")

    background_task = lambda filepath, file_id: el_client.audio_file_to_text(file_id, filepath)
    background.add_task(background_task, file.file_name, file_id)
    return {"ok": True}
