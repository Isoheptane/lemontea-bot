from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

from . lib.player import *
from . lib.rank import rank_name

async def player(bot: Bot, event:MessageEvent, args: Message):

    text_args = str(args).strip().split(" ")

    if len(args) >= 2 and args[1].type == "at":
        info, status = await get_player_info("qq", args[1].data["qq"], b50 = False)
    elif len(text_args) <= 1:
        info, status = await get_player_info("qq", event.user_id, b50 = False)
    else:
        info, status = await get_player_info("username", text_args[1], b50 = False)
        if (status == 400):
            try:
                info, status = await get_player_info("qq", int(text_args[1]), b50 = False)
            except:
                info, status = None, 400
    
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