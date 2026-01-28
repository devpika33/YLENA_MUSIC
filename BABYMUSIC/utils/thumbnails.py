YOUTUBE_THUMB_BASE = "https://i.ytimg.com/vi_webp"

async def get_thumb(videoid: str, chat_id=None):
    return f"{YOUTUBE_THUMB_BASE}/{videoid}/maxresdefault.webp"

