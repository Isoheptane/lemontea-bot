import os
from pathlib import Path
from io import BytesIO
import math
from unittest import result

from . performance import Performance
from . player import Player
from . cover import get_cover
from . import rating

from PIL import ImageFont, ImageDraw, Image

from .. path import picture_path

b40_bg = Image.open(picture_path.joinpath("b40_bg.png"))
b50_bg = Image.open(picture_path.joinpath("b50_bg.png"))

montserrat_bold = str(Path(os.path.dirname(__file__)).joinpath("static", "font", "Montserrat-Bold.ttf"))
montserrat_semibold = str(Path(os.path.dirname(__file__)).joinpath("static", "font", "Montserrat-SemiBold.ttf"))
notosans_bold = str(Path(os.path.dirname(__file__)).joinpath("static", "font", "NotoSansSC-Bold.otf"))
notosans_regular = str(Path(os.path.dirname(__file__)).joinpath("static", "font", "NotoSansSC-Regular.otf"))

title_font          = ImageFont.truetype(notosans_bold, 20)
score_font          = ImageFont.truetype(montserrat_bold, 32)
rank_font           = ImageFont.truetype(montserrat_bold, 24)
level_font          = ImageFont.truetype(montserrat_bold, 20)
rating_font         = ImageFont.truetype(montserrat_bold, 24)
name_font           = ImageFont.truetype(notosans_regular, 48)
info_font           = ImageFont.truetype(montserrat_semibold, 28)

chart_image = [
    Image.open(picture_path.joinpath(f"chart_basic.png")),
    Image.open(picture_path.joinpath(f"chart_advanced.png")),
    Image.open(picture_path.joinpath(f"chart_expert.png")),
    Image.open(picture_path.joinpath(f"chart_master.png")),
    Image.open(picture_path.joinpath(f"chart_remaster.png"))
]

rank_image = {
    "sssp"  : Image.open(picture_path.joinpath(f"rate_sssp.png")).resize((80, 40)),
    "sss"   : Image.open(picture_path.joinpath(f"rate_sss.png")).resize((80, 40)),
    "ssp"   : Image.open(picture_path.joinpath(f"rate_ssp.png")).resize((80, 40)),
    "ss"    : Image.open(picture_path.joinpath(f"rate_ss.png")).resize((80, 40)),
    "sp"    : Image.open(picture_path.joinpath(f"rate_sp.png")).resize((80, 40)),
    "s"     : Image.open(picture_path.joinpath(f"rate_s.png")).resize((80, 40)),
    "aaa"   : Image.open(picture_path.joinpath(f"rate_aaa.png")).resize((80, 40)),
    "aa"    : Image.open(picture_path.joinpath(f"rate_aa.png")).resize((80, 40)),
    "a"     : Image.open(picture_path.joinpath(f"rate_a.png")).resize((80, 40)),
    "bbb"   : Image.open(picture_path.joinpath(f"rate_bbb.png")).resize((80, 40)),
    "bb"    : Image.open(picture_path.joinpath(f"rate_bb.png")).resize((80, 40)),
    "b"     : Image.open(picture_path.joinpath(f"rate_b.png")).resize((80, 40)),
    "c"     : Image.open(picture_path.joinpath(f"rate_c.png")).resize((80, 40)),
    "d"     : Image.open(picture_path.joinpath(f"rate_d.png")).resize((80, 40))
}

combo_image = {
    "fc"    : Image.open(picture_path.joinpath(f"combo_fc.png")).resize((60, 40)),
    "fcp"   : Image.open(picture_path.joinpath(f"combo_fcp.png")).resize((60, 40)),
    "ap"    : Image.open(picture_path.joinpath(f"combo_ap.png")).resize((60, 40)),
    "app"   : Image.open(picture_path.joinpath(f"combo_app.png")).resize((60, 40))
}

sync_image = {
    "fs"    : Image.open(picture_path.joinpath(f"sync_fs.png")).resize((60, 40)),
    "fsp"   : Image.open(picture_path.joinpath(f"sync_fsp.png")).resize((60, 40)),
    "fsd"   : Image.open(picture_path.joinpath(f"sync_fsd.png")).resize((60, 40)),
    "fsdp"  : Image.open(picture_path.joinpath(f"sync_fsdp.png")).resize((60, 40))
}

diff_color = [
    (69, 193, 36),
    (255, 186, 1),
    (255, 90, 102),
    (134, 49, 200),
    (207, 144, 240)
]


def image_to_bytes(image: Image.Image, format = "PNG"):
    buffer = BytesIO()
    image.save(buffer, format)
    return buffer.getvalue()


def to_full_char(text: str) -> str:
    s: str = ""
    for c in text:
        if (ord(c) <= 255):
            s += chr(ord(c) + 65248)
        else:
            s += c
    return s