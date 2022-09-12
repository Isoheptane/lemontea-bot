from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.log import logger

import os
from pathlib import Path
from math import floor

from . lib.player import *
from . lib.image import image_to_bytes
from . lib.gen_best import generate_best

async def best(bot: Bot, event:MessageEvent, args: Message, b50: False):

    text_args = str(args).strip().split(" ")

    if len(args) >= 2 and args[1].type == "at":
        info, status = await get_player_info("qq", args[1].data["qq"], b50)
    elif len(text_args) <= 1:
        info, status = await get_player_info("qq", event.user_id, b50)
    else:
        info, status = await get_player_info("username", text_args[1], b50)
        if (status == 400):
            try:
                info, status = await get_player_info("qq", int(text_args[1]), b50)
            except:
                info, status = None, 400

    if status == -1:
        logger.error(f"Failed to get player info: {info}")
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text(f"获取玩家信息失败了呢……(Error: {info})")
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
    
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.image(image_to_bytes(await generate_best(info, b50)))
    ]))
    return
        