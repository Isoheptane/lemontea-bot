from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

from . best import best
from . query_player import player
from . query_song import query_song, query_chart

matcher = on_command("maimai", aliases = {"mai"})
@matcher.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):

    text_args = str(args).strip().split(" ")
    command = text_args[0]

    if (command == "help"):
        await help(bot, event, args)
    elif (command == "b40"):
        await best(bot, event, args, b50 = False)
    elif (command == "b50"):
        await best(bot, event, args, b50 = True)
    elif (command == "player"):
        await player(bot, event, args)
    elif (command == "tsong"):
        await query_song(bot, event, text_args, text = True)
    elif (command == "tchart"):
        await query_chart(bot, event, text_args, text = True)


async def help(bot: Bot, event:MessageEvent, message: Message):
    await bot.send(event, Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text("Lemon Bot maimai 帮助：\n"),
        MessageSegment.text("命令调用需要以\"/maimai\"或者\"/mai\"开头。\n"),
        MessageSegment.text("b40 [查分器用户名 | QQ | @消息] -查询用户的 Best 40 数据\n"),
        MessageSegment.text("b50 [查分器用户名 | QQ | @消息] -查询用户的 Best 50 数据\n"),
        MessageSegment.text("tsong <歌曲 ID> -查询歌曲信息\n"),
        MessageSegment.text("tchart <难度> <歌曲 ID> -查询谱面信息")
    ]))