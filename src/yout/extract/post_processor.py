import os

from yt_dlp.postprocessor.common import PostProcessor

from src.entity.file import File, FileState


class StorageInfoPP(PostProcessor):
    def __init__(self, file: File, downloader=None):
        super().__init__(downloader)
        self.file = file

    def run(self, information: dict) -> tuple[list[str], dict]:
        # check dict if needed
        # with open("/data/files/output.json", "w", encoding="utf-8") as f:
        #     json.dump(information, f, indent=4, sort_keys=True, default=str)
        self.file.channel_name = information.get("channel")
        self.file.name = information.get("title")
        self.file.duration = information.get("duration_string")

        # strip folder names from absolute path
        filename = information.get("filename")
        if filename:
            self.file.file_name = filename.removeprefix("/data/files/")
            self.file.size = information.get("filesize") or information.get("filesize_approx") or os.path.getsize(filename)

        # downloaded format instead of provided one
        format = information.get("format")
        if format:
            self.file.format = format
        self.file.state = FileState.end

        return [], information
