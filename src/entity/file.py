# from pydantic import field_validator
from datetime import UTC, datetime
from enum import StrEnum

from sqlmodel import TIMESTAMP, Field, SQLModel


class FileState(StrEnum):
    get = "get"
    start = "start"
    end = "end"
    error = "error"
    deleted = "deleted"


class FileBase(SQLModel):
    url: str = Field()
    format: str | None = Field(default=None)
    state: FileState = Field(default=FileState.get, index=True)
    download_duration: int | None = Field(default=None)  # in seconds

    channel_name: str | None = Field(default=None)
    file_name: str | None = Field(default=None)
    name: str | None = Field(default=None)
    size: int | None = Field(default=None)  # in bytes
    duration: str | None = Field(default=None)  # in youtube format e.g. 8:22 or 3:02:01

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(UTC),
        },
        sa_type=TIMESTAMP(timezone=True),
    )

    def size_mb(self) -> float | None:
        if self.size is None:
            return None
        return float(self.size) / 1024 / 1024


class CreateFile(FileBase):
    @staticmethod
    def is_valid_format(value: str) -> bool:
        return value in ["audio", "720", "360"]

    @staticmethod
    def is_valid_state(value: str) -> bool:
        try:
            FileState(value)
            return True
        except ValueError:
            return False


class File(FileBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
