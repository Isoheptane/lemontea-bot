from email import message
from nonebot import on_shell_command
from nonebot.params import ShellCommandArgv
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent
from nonebot.log import logger

from typing import Union, List

from . best import best
from . query_player import player
from . query_song import query_song, query_chart
from . custom import set_custom
from . scorelist import scorelist

matcher = on_shell_command("maimai", aliases = {"mai"})
@matcher.handle()
async def _(bot: Bot, event: MessageEvent, args: List[Union[str, MessageSegment]] = ShellCommandArgv()):
    
    command = str(args[0]).lower()

    if command == "help":
        await help(bot, event)
    elif command == "b40":
        await best(bot, event, args)
    elif command == "b50":
        await best(bot, event, args, b50 = True)
    elif command == "player":
        await player(bot, event, args)
    elif command == "tsong":
        await query_song(bot, event, args[1], text = True)
    elif command == "tchart":
        await query_chart(bot, event, args[1], text = True)
    elif command == "set":
        await set_custom(bot, event, args)
    elif command in ["scorelist", "分数列表", "scorelistid", "分数列表id"]:
        await scorelist(bot, event, args)


async def help(bot: Bot, event:MessageEvent):
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text("Lemon Bot maimai 帮助：\n"),
        MessageSegment.text("命令调用需要以\"/maimai\"或者\"/mai\"开头。\n"),
        MessageSegment.text("b40 [查分器用户名 | QQ | @消息] -查询用户的 Best 40 数据\n"),
        MessageSegment.text("b50 [查分器用户名 | QQ | @消息] -查询用户的 Best 50 数据\n"),
        MessageSegment.text("tsong <歌曲 ID> -查询歌曲信息\n"),
        MessageSegment.text("tchart <难度><歌曲 ID> -查询谱面信息")
    ]))