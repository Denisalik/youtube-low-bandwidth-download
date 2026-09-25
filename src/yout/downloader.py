import logging
import time

import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError

from src.entity.file import File, FileState

from .extract import StorageInfoPP

logger = logging.getLogger(__name__)


def download(file: File):
    link = file.url
    format = file.format
    logger.info("downloading file with format:%s url:%s", format, link)
    home_directory_path = "/data/files/"
    outtmpl = home_directory_path + file.id + "-" + "%(title)s.%(ext)s"
    ydl_opts = {"quiet": True, "format": format, "outtmpl": outtmpl}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            pp = StorageInfoPP(file=file, downloader=ydl)
            ydl.add_post_processor(pp, when="post_process")
            file.state = FileState.start
            start_time = time.perf_counter()
            ydl.download([link])
            took_time = time.perf_counter() - start_time
            file.download_duration = int(took_time)
        logger.info("Downloaded succefully, link: \n%s", link)
        return
    except DownloadError:
        logger.error("Download error")
        file.state = FileState.error
    except ExtractorError:
        logger.error("Extraction error")
        file.state = FileState.error
    except Exception:
        logger.exception("Unexpected error")
        file.state = FileState.error
        raise


def make_format(
    audio_only: bool = False, height: int = 720, smaller: bool = True, default_format: str = "135"
) -> str:
    """
    Examples:
        >>> make_format(False, 720, True)
        'bestvideo[height<=720]+bestaudio[format_note*=original]/best[height<=720]/135/139'
        >>> make_format(False, 360, False)
        'worstvideo[height>=360]+bestaudio[format_note*=original]/worst[height>=360]/135/139'
        >>> make_format(True)
        'ba[format_note*=original][format_id^=139]/139'

    Arguments:
        audioOnly: make format which is downloading only audio with id=139.
            Audio formats sorted by size in asc: 139, 249, 250, 140, 251.
        height: if video is downloaded, this param allow you to choose resolution.
            Chooses height, which is usually what everyone is using to show.
        smaller: if video is downloaded, this param allow you to choose resolution.
            Chooses best of heights if True, worst of heights if False.
        default_format: If video cannot be downloaded using your format, default format is used.
            When no specified default is 135(mp4, 480x854, shorts) + 139(audio only, streams).
    Returns:
        Format in string.
    """
    if audio_only:
        audio_format = "ba[format_note*=original][format_id^=139]" + "/139"
        return audio_format
    adjective = "best" if smaller else "worst"
    sign = "<=" if smaller else ">="
    formats = [
        f"{adjective}video[height{sign}{height}]+bestaudio[format_note*=original]",
        f"{adjective}[height{sign}{height}]",
        default_format,
        "139",
    ]
    return "/".join(formats)
