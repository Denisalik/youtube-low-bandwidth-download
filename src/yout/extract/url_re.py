import re
from pydantic import BaseModel

YOUTUBE_CHANNEL_RE = re.compile(
    r"https?://(?:www\.)?youtube\.com/"
    r"(?:"
    r"@(?P<handle>[\w.\-]+)"
    r"|channel/(?P<channel_id>UC[\w\-]+)"
    r"|c/(?P<custom>[\w.\-]+)"
    r"|user/(?P<user>[\w.\-]+)"
    r")"
    r"(?:/(?P<tab>videos|shorts|streams|playlists|community|about))?"
    r"/?",
    re.IGNORECASE,
)

class Parsed_URL(BaseModel):
    handle: str | None
    channel_id: str | None
    custom: str | None
    user: str | None
    tab: str
    
    @property
    def name() -> str | None:
        return self.handle or self.channel_id or self.custom or self.user

def parse_channel_url(url: str) -> Parsed_URL | None:
    m = YOUTUBE_CHANNEL_RE.match(url)
    if not m:
        return None
    kwargs = {
        "handle":     m.group("handle"),
        "channel_id": m.group("channel_id"),
        "custom":     m.group("custom"),
        "user":       m.group("user"),
        "tab":        m.group("tab") or "home",
    }
    return Parsed_URL(**kwargs)