from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.log import logger

from typing import List, Union

from . lib.image import download_image
from . lib import user_custom as custom

async def set_custom(bot: Bot, event: MessageEvent, args: List[Union[str, MessageSegment]]):

    if len(args) < 3 or not isinstance(args[1], str):
        return
    if args[1] == "avatar" or args[1] == "bg":
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
                MessageSegment.text("设置该自定义项目需要提供图片呢。")
            ]))
        if args[1] == "avatar":
            custom.set_user_avatar(event.user_id, image)
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("成功设定了头像。")
            ]))
    elif args[1] == "title":
        if not isinstance(args[2], str):
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("设置该自定义项目需要提供文本呢。")
            ]))
            return
        if len(args[2]) >= 40:
            await bot.send(event, Message([
                MessageSegment.reply(event.message_id),
                MessageSegment.text("称号长度不能超过40字哦。")
            ]))
            return
        custom.set_user_title(event.user_id, args[2])
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("成功设定了称号。")
        ]))
        return