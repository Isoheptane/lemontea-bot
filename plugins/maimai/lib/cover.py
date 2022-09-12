from nonebot.log import logger
from PIL import Image

from ..path import cover_path, resource_path
from . image import download_image

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
        logger.info(f"Downloading cover {file_name}...")
        try:
            cover = await download_image(download_path)
            cover.save(str(file_path))
        except:
            logger.info(f"Failed to download cover {file_name}...")
    
    if file_path.exists():
        return Image.open(file_path)
    else:
        logger.error(f"Failed to load cover {file_name}.")
        return default_cover