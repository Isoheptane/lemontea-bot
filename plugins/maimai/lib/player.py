import aiohttp

from typing import Dict, Optional, Tuple, List

from . performance import Performance

class Player:
    nickname: str
    username: str
    base_rating: int
    rank_rating: int
    chart_new: List[Performance]
    chart_old: List[Performance]

    def __init__(self, data: Dict):
        self.nickname       = data["nickname"]
        self.username       = data["username"]
        self.base_rating    = data["rating"]
        self.rank_rating    = data["additional_rating"]

        self.chart_new = []
        self.chart_old = []

        for chartData in data["charts"]["dx"]:
            self.chart_new.append(Performance(chartData))
        for chartData in data["charts"]["sd"]:
            self.chart_old.append(Performance(chartData))


async def get_player_info(type: str, id: str, b50: bool) -> Tuple[Optional[Player], int]:
    
    request = {type: id, "b50": True} if b50 else {type: id}
    
    try:
        async with aiohttp.request(
            "POST", 
            "https://www.diving-fish.com/api/maimaidxprober/query/player",
            json = request
        ) as response:
            if response.status == 400:
                return None, 400
            if response.status == 403:
                return None, 403
            data = await response.json()
            info = Player(data)
            return info, response.status
    except:
        return None, -1