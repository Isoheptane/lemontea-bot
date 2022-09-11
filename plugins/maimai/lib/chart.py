
from typing import Dict

class Chart():
    chart_id: int
    level: float
    level_display: str

    tap_count: int
    hold_count: int
    slide_count: int
    touch_count: int
    break_count: int
    charter: str

    def __init__(self, data: Dict, cid: int, level: float, level_display: float):
        self.chart_id       = cid
        self.level          = level
        self.level_display  = level_display
        
        self.tap_count      = data["notes"][0]
        self.hold_count     = data["notes"][1]
        self.slide_count    = data["notes"][2]
        self.touch_count    = data["notes"][3] if len(data["notes"]) == 5 else 0
        self.break_count    = data["notes"][-1]
        self.charter        = data["charter"]

diff_name = ["Basic", "Advanced", "Expert", "Master", "Re:MASTER"]

diff_name_index = {
    "绿": 0,
    "basic": 0,
    "黄": 1,
    "advanced": 1,
    "红": 2,
    "expert": 2,
    "紫": 3,
    "master": 3,
    "白": 4,
    "remaster": 4,
    "re:master": 4,
}