from pydantic import BaseModel


class Format(BaseModel):
    id: str
    extension: str
    resolution: str
    video_size: str


class FormatList(BaseModel):
    size: int
    formats: list[Format]
    url: str
    title: str


class ChannelVideo(BaseModel):
    title: str
    url: str


class ChannelList(BaseModel):
    size: int
    videos: list[ChannelVideo]
    channel_name: str


class DiskFile(BaseModel):
    size: int
    name: str
