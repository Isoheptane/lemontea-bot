import os
from pathlib import Path

resource_path = Path(os.path.dirname(__file__)).joinpath("resources")

cover_path = resource_path.joinpath("cover")

picture_path = resource_path.joinpath("pic")

custom_path = resource_path.joinpath("user_custom")