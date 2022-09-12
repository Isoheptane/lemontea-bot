from io import BytesIO
from PIL import Image

from .. path import resource_path

montserrat_bold     = str(resource_path.joinpath("font", "Montserrat-Bold.ttf"))
montserrat_semibold = str(resource_path.joinpath("font", "Montserrat-SemiBold.ttf"))
notosans_bold       = str(resource_path.joinpath("font", "NotoSansSC-Bold.otf"))
notosans_regular    = str(resource_path.joinpath("font", "NotoSansSC-Regular.otf"))

def image_to_bytes(image: Image.Image, format = "PNG"):
    buffer = BytesIO()
    image.save(buffer, format)
    return buffer.getvalue()