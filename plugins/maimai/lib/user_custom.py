import io
import json
import base64
from lib2to3.pgen2.token import OP
from PIL import Image
from typing import Any, Dict, Optional

from .. path import custom_path

class UserData:
    avatar: Optional[Image.Image]
    frame: Optional[Image.Image]
    title: Optional[str]

    def __init__(self):
        self.avatar = None
        self.frame = None
        self.title = None

def get_user_custom(id: int) -> UserData:
    data = UserData()
    user_path = custom_path.joinpath(f"{str(id)}.json")
    if not user_path.exists():
        return data

    file = open(user_path, mode = "r")
    profile: Dict[Any, Any] = json.load(file)
    file.close()

    if "avatar" in profile:
        avatar_data = base64.b64decode(profile["avatar"])
        data.avatar = Image.open(io.BytesIO(avatar_data))
    if "frame" in profile:
        frame_data = base64.b64decode(str(profile["frame"]))
        data.frame = Image.open(io.BytesIO(frame_data))
    if "title" in profile:
        data.title = profile["title"]
    
    return data

def set_user_data(id: int, key: str, value: Any):
    user_path = custom_path.joinpath(f"{str(id)}.json")
    if user_path.exists():
        file = open(user_path, mode = "r")
        profile: Dict[Any, Any] = json.load(file)
        file.close()
    else:
        profile: Dict[Any, Any] = {}

    profile[key] = value
    file = open(user_path, mode = "w")
    file.write(json.dumps(profile))
    file.close()

def unset_user_data(id: int, key: str):
    user_path = custom_path.joinpath(f"{str(id)}.json")
    if user_path.exists():
        file = open(user_path, mode = "r")
        profile: Dict[Any, Any] = json.load(file)
        file.close()
    else:
        profile: Dict[Any, Any] = {}

    profile.pop(key)
    file = open(user_path, mode = "w")
    file.write(json.dumps(profile))
    file.close()