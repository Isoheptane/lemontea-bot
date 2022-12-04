import math

from .. path import picture_path
from . image import *
from . gen_performance import generate_performance
from . gen_rating import generate_rating
from . player import Player
from . rating import compute_rating_new
from . user_custom import UserData

from PIL import ImageFont, ImageDraw, Image

name_font   = ImageFont.truetype(notosans_regular, 36)
info_font   = ImageFont.truetype(montserrat_semibold, 24)
title_font   = ImageFont.truetype(notosans_regular, 24)

b40_bg = Image.open(picture_path.joinpath("b40_bg.png"))
b50_bg = Image.open(picture_path.joinpath("b50_bg.png"))
avatar_mask = Image.open(picture_path.joinpath("avatar_mask.png")).split()[0]

def to_full_char(text: str) -> str:
    s: str = ""
    for c in text:
        if (ord(c) <= 255):
            s += chr(ord(c) + 65248)
        else:
            s += c
    return s


async def generate_best(info: Player, b50: bool, custom: UserData
) -> Image.Image:
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
    # Draw user name
    if not custom.avatar is None:
        result.paste(custom.avatar.resize((180, 180)), (510, 50), mask = avatar_mask)
    # Draw b40/b50 info
    draw.text(
        (725, 147), 
        to_full_char(info.nickname), 
        font = name_font, 
        anchor = "lm", 
        fill = (63, 63, 63)
    )
    if custom.title != None:
        draw.text(
            (935, 208), 
            custom.title,
            font = title_font, 
            anchor = "mm", 
            fill = (63, 63, 63), 
        )
    else:
        draw.text(
            (935, 210), 
            f"Best 50 Simulation" if b50 else
            f"Best 40: {info.base_rating} + {info.rank_rating}",
            font = info_font, 
            anchor = "mm", 
            fill = (63, 63, 63), 
        )
    # Draw DX Rating
    rating_image = generate_rating(base_rating if b50 else (info.base_rating + info.rank_rating), b50)
    result.paste(rating_image, (700, 40), mask = rating_image.split()[3])

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