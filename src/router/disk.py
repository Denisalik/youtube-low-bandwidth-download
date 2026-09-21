from pathlib import Path

from fastapi import APIRouter

from src.yout import DiskFile

router = APIRouter(
    prefix="/api/disk",
    tags=["disk"],
    responses={404: {"description": "Not found"}},
)

FILES_DIR = Path("/data/files")


@router.get("", response_model=list[DiskFile])
def get_disk_files():
    if not FILES_DIR.exists():
        return []
    files = [get_disk_file(f) for f in FILES_DIR.iterdir() if f.is_file()]
    return files


def get_disk_file(f: Path):
    return DiskFile(name=f.name, size=f.stat().st_size)
