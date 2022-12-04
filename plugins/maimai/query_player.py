import imp
from fastapi import FastAPI
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

from typing import List, Union

from . lib.player import *
from . lib.rank import rank_name

async def player(bot: Bot, event:MessageEvent, args: List[Union[str, MessageSegment]]):

    if len(args) >= 2:
        if isinstance(args[1], MessageSegment) and args[1].type == "at":
            qid = args[1].data["qq"]
            info, status = await get_player_info("qq", qid, b50 = False)
        else:
            info, status = await get_player_info("username", args[1], b50 = False)
            if (status == 400):
                info, status = await get_player_info("qq", args[1], b50 = False)
    
    if status == -1:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("获取玩家信息失败。")
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

    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text(f"昵称：{info.nickname}\n"),
        MessageSegment.text(f"用户名：{info.username}\n"),
        MessageSegment.text(f"DX Rating：{info.base_rating + info.rank_rating}\n"),
        MessageSegment.text(f"Rating：{info.base_rating}\n"),
        MessageSegment.text(f"段位：{rank_name[info.rank_rating]} ({info.rank_rating})")
    ]))