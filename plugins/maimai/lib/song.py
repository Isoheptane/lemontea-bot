from nonebot.log import logger

import json
from typing import Dict, List
import requests

from . chart import Chart
from .. path import resource_path

class Song:
    song_id: int
    title: str
    artist: str
    genre: str
    version: str
    release_date: str
    bpm: float
    is_new: bool

    dx_chart: bool
    charts: List[Chart] = []

    def __init__(self, data: Dict):
        self.song_id        = int(data["id"])
        self.title          = data["basic_info"]["title"]
        self.artist         = data["basic_info"]["artist"]
        self.genre          = data["basic_info"]["genre"]
        self.version        = data["basic_info"]["from"]
        self.release_date   = data["basic_info"]["release_date"]
        self.bpm            = float(data["basic_info"]["bpm"])
        self.is_new         = data["basic_info"]["is_new"]
        self.dx_chart       = True if data["type"] == "DX" else False

        self.charts = []
        index = 0
        for chart in data["charts"]:
            self.charts.append(Chart(chart, data["cids"][index], data["ds"][index], data["level"][index]))
            index += 1


song_list: Dict[int, Song] = {}

file_path = resource_path.joinpath("song_list.json")

if not file_path.exists():
    logger.info(f"Downloading song list...")
    response = requests.get("https://www.diving-fish.com/api/maimaidxprober/music_data")
    if response.status_code == 200:
        with file_path.open('wb') as file:
            file.write(response.content)
            file.close()
            logger.info(f"Successfully downloaded song list .")
    else:
        logger.error(f"Failed to download song list : Response code: {response.status}")

if file_path.exists():
    cache_file = open(file_path, "r")
    song_data = json.loads(cache_file.read())
    cache_file.close()
    for data in song_data:
        song_list[int(data["id"])] = Song(data)
