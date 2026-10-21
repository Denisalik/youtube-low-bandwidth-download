import pytest
import yt_dlp
import time
import random
from yt_dlp.utils import DownloadError, ExtractorError

from src.yout.downloader import make_format
from src.yout.extract.channel import list_channel_videos
from src.yout.extract.format import list_formats
            

def download(link: str, format: str, max_attempts: int = 10):
    home_directory_path = '~/Downloads/'
    link_id = round(random.uniform(0, 1), 2)
    outtmpl = home_directory_path + f'{link_id}-' + '%(title)s.%(ext)s'
    ydl_opts = {'quiet': True, 'format': format, 'outtmpl': outtmpl}
    # 'cookiefile': cookies_file,
    for attempt in range(max_attempts):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            print(f"Downloaded succefully, links: {link}")
            return
        except DownloadError:
            print(f"Download error (attempt {attempt + 1}/{max_attempts}):")
            time.sleep(3)
        except ExtractorError:
            print(f"Extraction error (attempt {attempt + 1}/{max_attempts}):")
        except Exception:
            print(f"Unexpected error")
            break
    print("Download failed after all attempts")
    return

@pytest.mark.skip(reason="uncomment me if needed")
def test_yt_dlp():
    download_links = []
    extract_links = []
    channel_links = []
    additional_links = []

    extract_links.extend(additional_links)

    for link in channel_links:
        data = list_channel_videos(link)
        print(data)
    for link in extract_links:
        data = list_formats(link, False)
        print(data)
    for link in download_links:
        format = make_format(False, 720, True)
        download(link, format, 1)
