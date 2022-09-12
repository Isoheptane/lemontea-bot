import math

from .. path import picture_path
from . image import *
from . gen_performance import generate_performance
from . player import Player
from . rating import compute_rating_new

from PIL import ImageFont, ImageDraw, Image

name_font   = ImageFont.truetype(notosans_regular, 48)
info_font   = ImageFont.truetype(montserrat_semibold, 28)

b40_bg = Image.open(picture_path.joinpath("b40_bg.png"))
b50_bg = Image.open(picture_path.joinpath("b50_bg.png"))

def to_full_char(text: str) -> str:
    s: str = ""
    for c in text:
        if (ord(c) <= 255):
            s += chr(ord(c) + 65248)
        else:
            s += c
    return s


async def generate_best(info: Player, b50: bool) -> Image.Image:

    result = b50_bg.copy() if b50 else b40_bg.copy()

    base_rating = 0

    for performance in info.chart_old:
        if b50:
            performance.rating = compute_rating_new(performance.level, performance.achievements)
        base_rating += performance.rating

    for performance in info.chart_new:
        if b50:
            performance.rating = compute_rating_new(performance.level, performance.achievements)
        base_rating += performance.rating

    draw = ImageDraw.Draw(result)
    # Draw name
    draw.text(
        (500, 108), 
        to_full_char(info.nickname), 
        font = name_font, 
        anchor = "lm", 
        fill = (63, 63, 63)
    )

    if b50:
        draw.text(
            (755, 195), 
            f"Best 50 Simulation: {base_rating}", 
            font = info_font, 
            anchor = "mm", 
            fill = (63, 63, 63), 
        )
    else:
        draw.text(
            (755, 195), 
            f"Best 40: {info.base_rating} + {info.rank_rating}", 
            font = info_font, 
            anchor = "mm", 
            fill = (63, 63, 63), 
        )

    # Draw best 25 / 35
    old_count = 0
    for chart in info.chart_old:
        chart_image = await generate_performance(chart, old_count + 1)
        place_x = int(old_count % 5) * 400 + 45
        place_y = math.floor(old_count / 5) * 125 + 275
        result.paste(chart_image, (place_x, place_y), mask = chart_image.split()[3])
        chart_image.close()
        old_count += 1

    if b50:
        b15_count = 0
        for chart in info.chart_new:
            chart_image = await generate_performance(chart, b15_count + 1)
            place_x = int(b15_count % 5) * 400 + 45
            place_y = math.floor(b15_count / 5) * 125 + 1215
            result.paste(chart_image, (place_x, place_y), mask = chart_image.split()[3])
            chart_image.close()
            b15_count += 1
    else:
        b15_count = 0
        for chart in info.chart_new:
            chart_image = await generate_performance(chart, b15_count + 1)
            place_x = int(b15_count % 5) * 400 + 45
            place_y = math.floor(b15_count / 5) * 125 + 965
            result.paste(chart_image, (place_x, place_y), mask = chart_image.split()[3])
            chart_image.close()
            b15_count += 1
        
    return result