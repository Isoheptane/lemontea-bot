import os
from PIL import Image
from typing import Optional

from .. path import custom_path

class UserData:
    avatar: Optional[Image.Image]
    bg_image: Optional[Image.Image]
    title: Optional[str]

    def __init__(self, avatar, bg_image, title):
        self.avatar = avatar
        self.bg_image = bg_image
        self.title = title

def get_user_custom(id: int) -> UserData:
    user_path = custom_path.joinpath(str(id))
    data = UserData(None, None, None)
    if user_path.joinpath("avatar.png").exists():
        avatar = Image.open(user_path.joinpath("avatar.png"))
        data.avatar = avatar
    if user_path.joinpath("bg_image.png").exists():
        bg_image = Image.open(user_path.joinpath("bg_image.png"))
        data.bg_image = bg_image
    if user_path.joinpath("title").exists():
        title = open(user_path.joinpath("title"), encoding = "utf-8", mode = "r").read().rstrip()
        data.title = title
    return data

def set_user_avatar(id: int, avatar: Image.Image):
    user_path = custom_path.joinpath(str(id))
    if not user_path.exists():
        os.makedirs(user_path)
    avatar.save(user_path.joinpath("avatar.png"))

def set_user_bg_image(id: int, bg_image: Image.Image):
    user_path = custom_path.joinpath(str(id))
    if not user_path.exists():
        os.makedirs(user_path)
    bg_image.save(user_path.joinpath("bg_image.png"))

def set_user_title(id: int, title: str):
    user_path = custom_path.joinpath(str(id))
    if not user_path.exists():
        os.makedirs(user_path)
    open(user_path.joinpath("title"), encoding = "utf-8", mode = "w").write(title)