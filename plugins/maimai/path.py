import os
from pathlib import Path
from venv import create

resource_path = Path("./resources/maimai/")

cover_path = resource_path.joinpath("cover")

picture_path = resource_path.joinpath("pic")

data_path = Path("./data/maimai/")

custom_path = data_path.joinpath("user_custom")

cover_path.mkdir(parents = True, exist_ok = True)

custom_path.mkdir(parents = True, exist_ok = True)