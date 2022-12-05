import math

from .. path import picture_path
from . image import *
from . performance import Performance
from . gen_performance import generate_performance

from typing import List
from PIL import ImageFont, ImageDraw, Image

page_font = ImageFont.truetype(montserrat_semibold, 36)
single_line_font = ImageFont.truetype(montserrat_semibold, 36)
double_line_font = ImageFont.truetype(montserrat_semibold, 28)

bg = Image.open(picture_path.joinpath("scorelist.png"))

async def generate_scorelist(performances: List[Performance], level: str, score: str, cur_page: int, total_page: int) -> Image.Image:
    result = bg.copy()
    draw = ImageDraw.Draw(result)

    count = 0
    for p in performances:
        chart_image = await generate_performance(p, (cur_page - 1) * 20 + count + 1)
        place_x = int(count % 2) * 400 + 45
        place_y = math.floor(count / 2) * 125 + 125
        result.paste(chart_image, (place_x, place_y), mask = chart_image.split()[3])
        chart_image.close()
        count += 1

    draw.text(
        (750, 1465), 
        f"{cur_page} / {total_page}",
        font = page_font, 
        anchor = "mm", 
        fill = (76, 76, 76)
    )
    
    if score == None:
        draw.text(
            (335, 1465), 
            level,
            font = single_line_font, 
            anchor = "mm", 
            fill = (76, 76, 76)
        )
    else:
        draw.text(
            (335, 1445), 
            level,
            font = double_line_font, 
            anchor = "mm", 
            fill = (76, 76, 76)
        )
        draw.text(
            (335, 1485), 
            score,
            font = double_line_font, 
            anchor = "mm", 
            fill = (76, 76, 76)
        )

    return result