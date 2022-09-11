from typing import Dict

class Performance:
    title: str
    dx_chart: bool
    song_id: int

    difficulty: str
    difficulty_index: int
    level_display: str
    level: float

    achievements: float
    rate: str
    rating: int
    dx_score: int
    full_combo: str #fc #fcp #ap #app
    full_sync: str  #fs #fsp #fsd #fsdp

    def __init__(self, data: Dict):
        self.title              = data["title"]
        self.dx_chart           = data["type"] == "DX"
        self.song_id            = data["song_id"]
        self.difficulty         = data["level_label"]
        self.difficulty_index   = data["level_index"]
        self.level_display      = data["level"]
        self.level              = data["ds"]
        self.achievements       = data["achievements"]
        self.rate               = data["rate"]
        self.rating             = data["ra"]
        self.dx_score           = data["dxScore"]
        self.fc                 = data["fc"]
        self.fs                 = data["fs"]
