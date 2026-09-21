from yt_dlp.postprocessor.common import PostProcessor

from src.entity.file import File


class StorageInfoPP(PostProcessor):
    def __init__(self, file: File, downloader=None):
        super().__init__(downloader)
        self.file = file

    def run(self, info: dict) -> tuple[list, dict]:
        self.file.size = info["filesize"]
        self.file.channel_name = info["channel"]
        self.file.name = info["title"]
        self.file.duration = info["duration_string"]

        # strip folder names from absolute path
        self.file.file_name = info["filename"].removeprefix("/data/files/")

        # downloaded format instead of provided one
        self.file.format = info["format"]

        return [], info
