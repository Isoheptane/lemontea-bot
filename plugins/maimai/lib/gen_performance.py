from . performance import Performance
from . cover import get_cover

from .. path import picture_path
from . image import *

from PIL import ImageFont, ImageDraw, Image

title_font  = ImageFont.truetype(notosans_bold, 20)
score_font  = ImageFont.truetype(montserrat_bold, 32)
rank_font   = ImageFont.truetype(montserrat_bold, 24)
level_font  = ImageFont.truetype(montserrat_bold, 20)
rating_font = ImageFont.truetype(montserrat_bold, 24)

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

type_dx_image = Image.open(picture_path.joinpath(f"chart_type_dx.png"))
type_sd_image = Image.open(picture_path.joinpath(f"chart_type_sd.png"))

diff_color = [
    (69, 193, 36),
    (255, 186, 1),
    (255, 90, 102),
    (134, 49, 200),
    (207, 144, 240)
]

async def generate_performance(performance: Performance, rank: int) -> Image.Image:
    image = chart_image[performance.difficulty_index].copy()

    cover = await get_cover(performance.song_id)
    cover = cover.resize((90, 90))
    image.paste(cover, (25, 25))
    cover.close()

    image.paste(
        type_dx_image if performance.dx_chart else type_sd_image, 
        (68, 88), 
        type_dx_image.split()[3] if performance.dx_chart else type_sd_image.split()[3]
    )

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
    if performance.full_combo != "":
        image.paste(combo_image[performance.full_combo], (285, 82), combo_image[performance.full_combo].split()[3])
    if performance.full_sync != "":
        image.paste(sync_image[performance.full_sync], (323, 82), sync_image[performance.full_sync].split()[3])
    
    return image