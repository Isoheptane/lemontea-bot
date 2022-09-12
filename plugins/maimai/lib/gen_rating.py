import math
from .. path import picture_path
from . image import *

from PIL import ImageFont, ImageDraw, Image

rating_font = ImageFont.truetype(montserrat_bold, 32)

rating_bg = [
    Image.open(picture_path.joinpath("rating_white.png")),
    Image.open(picture_path.joinpath("rating_blue.png")),
    Image.open(picture_path.joinpath("rating_green.png")),
    Image.open(picture_path.joinpath("rating_yellow.png")),
    Image.open(picture_path.joinpath("rating_red.png")),
    Image.open(picture_path.joinpath("rating_purple.png")),
    Image.open(picture_path.joinpath("rating_copper.png")),
    Image.open(picture_path.joinpath("rating_silver.png")),
    Image.open(picture_path.joinpath("rating_gold.png")),
    Image.open(picture_path.joinpath("rating_rainbow.png")),
]

def get_rating_bg(rating: int, b50: bool) -> Image.Image:
    index = 0
    if (rating >= (1000 if b50 else 1000)):
        index += 1
    if (rating >= (2000 if b50 else 2000)):
        index += 1
    if (rating >= (4000 if b50 else 3000)):
        index += 1
    if (rating >= (7000 if b50 else 4000)):
        index += 1
    if (rating >= (10000 if b50 else 5000)):
        index += 1
    if (rating >= (12000 if b50 else 6000)):
        index += 1
    if (rating >= (13000 if b50 else 7000)):
        index += 1
    if (rating >= (14000 if b50 else 8000)):
        index += 1
    if (rating >= (15000 if b50 else 9000)):
        index += 1
    return rating_bg[index].copy()

def generate_rating(rating: int, b50: bool) -> Image.Image:
    result = get_rating_bg(rating, b50)
    draw = ImageDraw.Draw(result)
    if (rating >= 0):
        draw.text((255, 38), f"{math.floor(rating % 10)}", font = rating_font, anchor = "rm", fill = (255, 222, 68), stroke_fill = (0, 0, 0), stroke_width = 3)
    if (rating >= 10):
        draw.text((231, 38), f"{math.floor(rating / 10 % 10)}", font = rating_font, anchor = "rm", fill = (255, 222, 68), stroke_fill = (0, 0, 0), stroke_width = 3)
    if (rating >= 100):
        draw.text((207, 38), f"{math.floor(rating / 100 % 10)}", font = rating_font, anchor = "rm", fill = (255, 222, 68), stroke_fill = (0, 0, 0), stroke_width = 3)
    if (rating >= 1000):
        draw.text((183, 38), f"{math.floor(rating / 1000 % 10)}", font = rating_font, anchor = "rm", fill = (255, 222, 68), stroke_fill = (0, 0, 0), stroke_width = 3)
    if (rating >= 10000):
        draw.text((159, 38), f"{math.floor(rating / 10000 % 10)}", font = rating_font, anchor = "rm", fill = (255, 222, 68), stroke_fill = (0, 0, 0), stroke_width = 3)
    return result