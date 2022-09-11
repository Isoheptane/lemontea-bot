from nonebot.log import logger
import aiohttp
from typing import Tuple
from PIL import Image

from ..path import cover_path, resource_path

default_cover = Image.open(resource_path.joinpath("default_cover.png"))

if not cover_path.exists():
    cover_path.mkdir()

async def get_cover(id: int) -> Image.Image:
    if id >= 10001:
        id -= 10000

    file_name = f"{id:04d}.png"
    file_path = cover_path.joinpath(file_name)

    if not file_path.exists():
        # Auto download cover from diving fish's site
        download_path = "https://www.diving-fish.com/covers/" + file_name
        logger.info(f"Downloading cover {file_name} ...")

        async with aiohttp.request("GET", download_path) as response:
            if response.status != 200:
                logger.error(f"Failed to download from {download_path} : Response code: {response.status}")
                return None
            with file_path.open('wb') as cover_file:
                data = await response.content.read()
                cover_file.write(data)
                cover_file.close()
            logger.info(f"Successfully downloaded cover {file_name} .")
    
    if file_path.exists():
        return Image.open(file_path)
    else:
        logger.error(f"Failed to load cover {file_name} .")
        return default_cover