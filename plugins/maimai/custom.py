from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.log import logger

import base64
from typing import List, Union

from . lib.image import download_image, image_to_bytes
from . lib import user_custom as custom

async def set_custom(bot: Bot, event: MessageEvent, args: List[Union[str, MessageSegment]]):
    if len(args) < 3 or not isinstance(args[1], str):
        return
    if args[1] == "avatar":
        await set_avatar(bot, event, args)
    elif args[1] == "frame":
        await set_frame(bot, event, args)
    elif args[1] == "title":
        await set_title(bot, event, args)

async def set_avatar(bot: Bot, event: MessageEvent, args: List[Union[str, MessageSegment]]):
    if not isinstance(args[2], MessageSegment) or args[2].type != "image":
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("设置该自定义项目需要提供图片呢。")
        ]))
        return

    image_url = args[2].data["url"]
    image = await download_image(image_url)

    if isinstance(image, Exception):
        logger.warning(f"Failed to download image. ({type(image).__module__}.{type(image).__name__}: {image})")
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("图片下载失败。")
        ]))
        return
    custom.set_user_data(
        event.user_id, 
        "avatar",
        base64.b64encode(image_to_bytes(image.resize((180, 180)))).decode(encoding = "utf-8")
    )
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text("成功设定了头像。")
    ]))

async def set_frame(bot: Bot, event: MessageEvent, args: List[Union[str, MessageSegment]]):
    if not isinstance(args[2], MessageSegment) or args[2].type != "image":
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("设置该自定义项目需要提供图片呢。")
        ]))
        return

    image_url = args[2].data["url"]
    image = await download_image(image_url)

    if isinstance(image, Exception):
        logger.warning(f"Failed to download image. ({type(image).__module__}.{type(image).__name__}: {image})")
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("图片下载失败。")
        ]))
        return
    custom.set_user_data(
        event.user_id, 
        "frame",
        base64.b64encode(image_to_bytes(image.resize((1250, 200)))).decode(encoding = "utf-8")
    )
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text("成功设定了姓名框。")
    ]))

async def set_title(bot: Bot, event: MessageEvent, args: List[Union[str, MessageSegment]]):
    title = ""
    for i in range(2, len(args)):
        if (isinstance(args[i], str)):
            title = title + args[i] + " "
    title = title.strip()

    if len(title) >= 30:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("称号长度不能超过 30 字哦。")
        ]))
        return  
    custom.set_user_data(
        event.user_id, 
        "title",
        title
    )
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text("成功设定了称号。")
    ]))