from . performance import Performance
from . cover import get_cover

from . image import *

from PIL import ImageFont, ImageDraw, Image

async def generate_performance(performance: Performance, rank: int) -> Image.Image:
    image = chart_image[performance.difficulty_index].copy()

    cover = await get_cover(performance.song_id)
    cover = cover.resize((90, 90))
    image.paste(cover, (25, 25))
    cover.close()

    draw = ImageDraw.Draw(image)

    title_image = Image.new("RGBA", (240, 30), (0, 0, 0, 0))

    title_draw = ImageDraw.Draw(title_image)
    title_draw.text((0, 23), performance.title, font = title_font, anchor = "ls")
    image.paste(title_image, (130, 23), title_image.split()[3])

    draw.text((135, 80), f"{performance.achievements:.4f}%", font = score_font, anchor = "ls")
    draw.text((130, 111), f"#{rank}", font = rank_font, anchor = "ls", fill = diff_color[performance.difficulty_index])
    draw.text((230, 111), f"{performance.level:.1f}", font = level_font, anchor = "rs", fill = diff_color[performance.difficulty_index])
    draw.text((231, 102), "▶", font = rating_font, anchor = "lm", fill = diff_color[performance.difficulty_index])
    draw.text((248, 111), f"{performance.rating}", font = rating_font, anchor = "ls", fill = diff_color[performance.difficulty_index])
    image.paste(rank_image[performance.rate], (305, 49), rank_image[performance.rate].split()[3])
    if performance.fc != "":
        image.paste(combo_image[performance.fc], (285, 82), combo_image[performance.fc].split()[3])
    if performance.fs != "":
        image.paste(sync_image[performance.fs], (323, 82), sync_image[performance.fs].split()[3])
    
    return image