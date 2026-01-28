import os, aiohttp, asyncio
from PIL import Image
from io import BytesIO

# ---------- CONFIG ----------
BASE = "https://i.ytimg.com/vi_webp"
DIR = "tcache"
os.makedirs(DIR, exist_ok=True)

RAM = {}          # videoid -> path
LOCKS = {}        # videoid -> asyncio.Lock
HEADERS = {"User-Agent": "Mozilla/5.0"}

# ---------- INTERNAL FETCH ----------
async def _fetch_and_convert(videoid: str) -> str:
    url = f"{BASE}/{videoid}/maxresdefault.webp"
    path = f"{DIR}/{videoid}.jpg"

    async with aiohttp.ClientSession(headers=HEADERS) as s:
        async with s.get(url, timeout=10) as r:
            if r.status != 200:
                raise RuntimeError("Thumbnail HTTP error")
            data = await r.read()
            if len(data) < 1024:
                raise RuntimeError("Empty thumbnail")

    Image.open(BytesIO(data)).convert("RGB").save(
        path,
        "JPEG",
        quality=95,
        subsampling=0,
        optimize=True
    )

    RAM[videoid] = path
    return path

# ---------- PUBLIC API ----------
async def get_thumb(videoid: str, chat_id=None) -> str:
    # 1️⃣ RAM cache (fastest)
    if videoid in RAM:
        return RAM[videoid]

    path = f"{DIR}/{videoid}.jpg"

    # 2️⃣ Disk cache
    if os.path.exists(path):
        RAM[videoid] = path
        return path

    # 3️⃣ Lock per video (no duplicate download)
    lock = LOCKS.setdefault(videoid, asyncio.Lock())

    async with lock:
        # re-check after wait
        if videoid in RAM:
            return RAM[videoid]
        if os.path.exists(path):
            RAM[videoid] = path
            return path

        # fetch + convert (WAIT here)
        return await _fetch_and_convert(videoid)
