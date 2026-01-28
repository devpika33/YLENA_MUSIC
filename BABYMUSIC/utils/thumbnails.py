import os, asyncio, aiohttp
from PIL import Image
from io import BytesIO

BASE = "https://i.ytimg.com/vi_webp"
DIR = "tcache"; os.makedirs(DIR, exist_ok=True)

RAM = {}        # videoid -> path
BUSY = set()    # in-progress guard

async def _warm(videoid):
    if videoid in BUSY: return
    BUSY.add(videoid)
    try:
        url = f"{BASE}/{videoid}/maxresdefault.webp"
        path = f"{DIR}/{videoid}.jpg"
        async with aiohttp.ClientSession(
            headers={"User-Agent": "Mozilla/5.0"}
        ) as s:
            async with s.get(url, timeout=10) as r:
                if r.status != 200: return
                d = await r.read()
                if len(d) < 1024: return
        Image.open(BytesIO(d)).convert("RGB") \
            .save(path, "JPEG", quality=95, subsampling=0, optimize=True)
        RAM[videoid] = path
    finally:
        BUSY.discard(videoid)

async def get_thumb(videoid: str, chat_id=None):
    if videoid in RAM:                # ~0.1–1 ms
        return RAM[videoid]

    path = f"{DIR}/{videoid}.jpg"
    if os.path.exists(path):          # ~2–5 ms
        RAM[videoid] = path
        return path

    asyncio.create_task(_warm(videoid))  # background
    return None                         # instant return
