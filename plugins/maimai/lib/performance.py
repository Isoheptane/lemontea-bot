from typing import Dict

from tomlkit import boolean

from . song import Song, song_list
from . achievements import compute_rate, compute_rating

class Performance:
    song_id: int
    title: str
    dx_chart: bool

    difficulty_index: int
    level: float

    achievements: float
    rate: str
    rating: int
    full_combo: str #fc #fcp #ap #app
    full_sync: str  #fs #fsp #fsd #fsdp

    def __init__(
        self, id: int, 
        level_index: int,
        achievements: float, 
        fc: str, 
        fs: str
    ):
        self.song_id            = id
        self.title              = song_list[id].title
        self.dx_chart           = song_list[id].dx_chart
        self.difficulty_index   = level_index
        self.level              = song_list[id].charts[level_index].level
        self.achievements       = achievements
        self.rate               = compute_rate(achievements)
        self.rating             = compute_rating(self.level, achievements)
        self.full_combo         = fc
        self.full_sync          = fs