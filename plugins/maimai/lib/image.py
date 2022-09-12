from ast import Bytes
import re
import aiohttp
import requests
from io import BytesIO
from PIL import Image

from .. path import resource_path

montserrat_bold     = str(resource_path.joinpath("font", "Montserrat-Bold.ttf"))
montserrat_semibold = str(resource_path.joinpath("font", "Montserrat-SemiBold.ttf"))
notosans_bold       = str(resource_path.joinpath("font", "NotoSansSC-Bold.otf"))
notosans_regular    = str(resource_path.joinpath("font", "NotoSansSC-Regular.otf"))

def image_to_bytes(image: Image.Image, format = "PNG"):
    buffer = BytesIO()
    image.save(buffer, format)
    return buffer.getvalue()

async def download_image(url: str, timeout: float = 5.0) -> Image.Image:
    async with aiohttp.request(
        "GET", 
        url, 
        timeout = aiohttp.ClientTimeout(timeout)
    ) as response:
        data = await response.content.read()
        return Image.open(BytesIO(data))