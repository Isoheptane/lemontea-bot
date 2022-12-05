import math
import re

from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.log import logger

from PIL import Image
from typing import Union, List

from . lib.player import *
from . lib.image import image_to_bytes
from . lib.gen_scorelist import generate_scorelist

async def scorelist(bot: Bot, event:MessageEvent, args: List[Union[str, MessageSegment]]):
    level_filter: str = None
    score_filter: str = None
    page: int = 1

    command = args[0].lower()

    if command in ["scorelistid", "分数列表id"]:
        if isinstance(args[1], MessageSegment) and args[1].type == "at":
            info, status = await get_player_records("qq", args[1].data["qq"])
        else:
            info, status = await get_player_records("username", args[1])
            if (status == 400):
                qid = args[1]
                info, status = await get_player_records("qq", qid)
        if len(args) < 3 or not isinstance(args[2], str):
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("需要提供查询的难度或定数区间哦。")
            ]))
            return
        try:
            level_filter = args[2]
            if len(args) == 4:
                if args[3].isdigit():
                    page = int(args[3])
                else:
                    score_filter = args[3]
            elif len(args) == 5:
                score_filter = args[3]
                page = int(args[4])
        except:
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("参数格式不正确。")
            ]))
            return
    else:
        info, status = await get_player_records("qq", event.user_id)
        if len(args) < 2 or not isinstance(args[1], str):
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("需要提供查询的难度或定数区间哦。")
            ]))
            return
        try:
            level_filter = args[1]
            if len(args) == 3:
                if args[2].isdigit():
                    page = int(args[2])
                else:
                    score_filter = args[2]
            if len(args) == 4:
                score_filter = args[2]
                page = int(args[3])
        except:
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("参数格式不正确。")
            ]))
            return
    
    level_min = 0.0
    level_max = 15.0
    score_min = 0.0
    score_max = 101.0

    try:
        if "-" in level_filter or "~" in level_filter:
            levels = re.split("-|~", level_filter)
            level_min = float(levels[0])
            level_max = float(levels[1])
        elif level_filter.endswith("+"):
            level_base = float(level_filter.removesuffix("+"))
            level_min = level_base + 0.7
            level_max = level_base + 0.9
        elif "." in level_filter:
            level_min = level_max = float(level_filter)
        else:
            level_min = float(level_filter)
            level_max = level_min + 0.6
        if level_min > level_max:
            raise
    except:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("等级的格式不正确。")
        ]))
        return

    if score_filter != None:
        try:
            if "-" in score_filter or "~" in score_filter:
                scores = re.split("-|~", score_filter)
                score_min = float(scores[0])
                score_max = float(scores[1])
            else:
                rate = score_filter.lower()
                if (rate == "d"):
                    score_min = 0.0
                    score_max = 49.9999
                elif (rate == "c"):
                    score_min = 50.0
                    score_max = 59.9999
                elif (rate == "b"):
                    score_min = 60.0
                    score_max = 69.9999
                elif (rate == "bb"):
                    score_min = 70.0
                    score_max = 74.9999
                elif (rate == "bbb"):
                    score_min = 75.0
                    score_max = 79.9999
                elif (rate == "a"):
                    score_min = 80.0
                    score_max = 89.9999
                elif (rate == "aa"):
                    score_min = 90.0
                    score_max = 93.9999
                elif (rate == "aaa"):
                    score_min = 94.0
                    score_max = 96.9999
                elif (rate == "s"):
                    score_min = 97.0
                    score_max = 97.9999
                elif (rate == "s+"):
                    score_min = 98.0
                    score_max = 98.9999
                elif (rate == "ss"):
                    score_min = 99.0
                    score_max = 99.4999
                elif (rate == "ss+"):
                    score_min = 99.5
                    score_max = 99.9999
                elif (rate == "sss"):
                    score_min = 100.0
                    score_max = 100.4999
                elif (rate == "sss+"):
                    score_min = 100.5
                    score_max = 101.0
            if score_min > score_max:
                raise
        except:
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("达成率区间的格式不正确。")
            ]))
            return

    if status == -1:
        logger.opt(colors = True, exception = info).error("Failed to get player info: Exception")
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text(f"获取玩家信息失败了呢……({type(info).__module__}.{type(info).__name__}: {info})")
        ]))
        return
    
    if status == 400:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("没有找到这个玩家呢。")
        ]))
        return
    
    if status == 403:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("该玩家禁止了其他人查询成绩。")
        ]))
        return

    if status != 200:
        logger.error(f"Failed to get player info: HTTP {status}")
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text(f"获取玩家信息失败了呢……(HTTP {status})")
        ]))
        return
        
    filtered: List[Performance] = []
    for p in list(info):
        if p.level < level_min or p.level > level_max:
            continue
        if p.achievements < score_min or p.achievements > score_max:
            continue
        filtered.append(p)
    
    filtered.sort(key = lambda p : (p.achievements, p.level), reverse = True)
    paged = filtered[(page - 1) * 20 : min(page * 20, len(filtered))]

    level_display = ""
    if "-" in level_filter:
        level_display += f"Difficulty: {level_min:.1f}~{level_max:.1f}"
    else:
        level_display += f"Difficulty: {level_filter}"

    score_display = None
    if score_filter != None:
        score_display = ""
        if "-" in score_filter:
            score_display += f"Achievements: {score_min:.4f}%~{score_max:.4f}%"
        else:
            score_display += f"Rank: {score_filter.upper()}"

    image = await generate_scorelist(
        paged, 
        level_display,
        score_display,
        page,
        math.ceil(float(len(filtered)) / 20)
    )

    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.image(image_to_bytes(image))
    ]))
    
    return
        