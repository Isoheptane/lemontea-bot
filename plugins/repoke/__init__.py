from time import time
from nonebot import on_notice
from nonebot.adapters import Event, Bot
from nonebot.adapters.onebot.v11 import Event, PokeNotifyEvent, Message, MessageSegment

def check_poke(event: Event):
    if isinstance (event, PokeNotifyEvent):
        if (event.target_id == event.self_id and event.user_id != event.self_id):
            return True
    return False

matcher = on_notice(rule = check_poke)

@matcher.handle()
async def on_poke(bot: Bot, event: PokeNotifyEvent):
    await bot.send(event, Message([
        MessageSegment(type = "poke", data = {"qq": event.user_id})
    ]))