import yt_dlp

from .model import Format, FormatList


def list_formats(url: str, audio_only: bool = False, no_size_ignore: bool = True) -> FormatList:
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        formats = []
        for fmt in info['formats']:
            vcodec = fmt.get('vcodec', 'N/A')
            format_id = fmt.get('format_id', 'N/A')
            ext = fmt.get('ext', 'N/A')
            if fmt.get('width', '?') != None:
                resolution = f"{fmt.get('width', '?')}x{fmt.get('height', '?')}"
            else:
                resolution = 'Audio'
            filesize = fmt.get('filesize')
            size_str = f"{filesize / 1024 / 1024:.1f} MB" if filesize else "N/A"
            if no_size_ignore and size_str == "N/A":
                continue
            if audio_only and vcodec != 'none':
                continue
            formats.append(Format(id=format_id, extension=ext, resolution=resolution, video_size=size_str))
        return FormatList(size=len(formats), formats=formats, url=url, title=info['title'])