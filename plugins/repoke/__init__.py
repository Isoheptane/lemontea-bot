from nonebot import on_notice
from nonebot.adapters import Event, Bot
from nonebot.adapters.onebot.v11 import Event, PokeNotifyEvent, Message, MessageSegment

def check_poke(event: Event):
    if isinstance (event, PokeNotifyEvent):
        if (event.target_id == event.self_id):
            return True
    return False

matcher = on_notice(rule = check_poke)

@matcher.handle()
async def repoke(bot: Bot, event: PokeNotifyEvent):
    if (event.target_id == event.self_id):
        await bot.send(event, Message([
            MessageSegment(type = "poke", data = {"qq": event.user_id})
        ]))