from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.log import logger

from PIL import Image
from typing import Union, List

from . lib.player import *
from . lib.image import download_image, image_to_bytes
from . lib.gen_best import generate_best
from . lib.user_custom import UserData, get_user_custom

async def best(bot: Bot, event:MessageEvent, args: List[Union[str, MessageSegment]], b50 = False):

    qid: int = None

    if len(args) >= 2:
        if isinstance(args[1], MessageSegment) and args[1].type == "at":
            qid = args[1].data["qq"]
            info, status = await get_player_info("qq", qid, b50)
        else:
            info, status = await get_player_info("username", args[1], b50)
            if (status == 400):
                qid = args[1]
                info, status = await get_player_info("qq", qid, b50)
    else:
        qid = event.user_id
        info, status = await get_player_info("qq", qid, b50)

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

    if not qid == None:
        custom = get_user_custom(qid)
        if custom.avatar == None:
            avatar = await download_image(f"https://q1.qlogo.cn/g?b=qq&nk={qid}&s=640", 10.0)
            if (isinstance(avatar, Image.Image)):
                custom.avatar = avatar
            else:
                logger.warning(f"Failed to download QQ avatar. ({type(avatar).__module__}.{type(avatar).__name__}: {avatar})")
                image = await generate_best(info, b50, custom)
        image = await generate_best(info, b50, custom)
    else:
        image = await generate_best(info, b50, UserData())
    
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.image(image_to_bytes(image))
    ]))
    return
        