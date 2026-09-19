import yt_dlp

from .model import ChannelList, ChannelVideo
from .url_re import parse_channel_url

def list_channel_videos(url: str) -> ChannelList:
    if not url.endswith('/videos'):
        url = url + '/videos'
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        videos = info.get('entries', [])
        channel_videos = [ChannelVideo(video['title'], f'https://www.youtube.com/watch?v={video['id']}') for video in videos]
        parsed_channel_name = parse_channel_url(url).name
        return ChannelList(size=len(channel_videos), videos=channel_videos, channel_name=parsed_channel_name)