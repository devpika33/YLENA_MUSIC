import os, aiohttp, asyncio
from PIL import Image
from io import BytesIO

BASE = "https://i.ytimg.com/vi_webp"
DIR = "tcache"; os.makedirs(DIR, exist_ok=True)
RAM, LOCKS = {}, {}

async def _fetch(videoid):
    url = f"{BASE}/{videoid}/maxresdefault.webp"
    path = f"{DIR}/{videoid}.jpg"
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            data = await r.read()
    Image.open(BytesIO(data)).convert("RGB") \
        .save(path, "JPEG", quality=95, subsampling=0, optimize=True)
    RAM[videoid] = path
    return path

async def get_thumb(videoid):
    if videoid in RAM:
        return RAM[videoid]
    path = f"{DIR}/{videoid}.jpg"
    if os.path.exists(path):
        RAM[videoid] = path
        return path
    lock = LOCKS.setdefault(videoid, asyncio.Lock())
    async with lock:
        if videoid in RAM:
            return RAM[videoid]
        if os.path.exists(path):
            RAM[videoid] = path
            return path
        return await _fetch(videoid)
