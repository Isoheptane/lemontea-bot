from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

from typing import List
import regex as regex

from . lib.cover import get_cover
from . lib.image import image_to_bytes
from . lib.song import Song, song_list
from . lib.chart import Chart, diff_name, diff_name_index

async def query_song(bot: Bot, event: MessageEvent, args: List[str], text: bool = False):
    try:
        song_id = int(args[1])
    except:
        return
    if not song_id in song_list:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("没有对应的歌曲呢。")
        ]))
        return
    song = song_list[song_id]

    if text:
        await bot.send(event, Message([
            MessageSegment.image(image_to_bytes(await get_cover(song.song_id))),
            MessageSegment.text(f"\n{song_id}. {song.title}\n"),
            MessageSegment.text(f"艺术家：{song.artist}\n"),
            MessageSegment.text(f"流派：{song.genre}\n"),
            MessageSegment.text(f"版本：{song.version}\n"),
            MessageSegment.text("谱面类型：" + ("DX" if song.dx_chart else "标准") + "\n"),
            MessageSegment.text(f"BPM：{song.bpm}\n"),
            MessageSegment.text(f"定数："),
            MessageSegment.text(f"{song.charts[0].level:.1f} / "),
            MessageSegment.text(f"{song.charts[1].level:.1f} / "),
            MessageSegment.text(f"{song.charts[2].level:.1f} / "),
            MessageSegment.text(f"{song.charts[3].level:.1f}"),
            MessageSegment.text(f" / {song.charts[4].level:.1f}" if len(song.charts) == 5 else "")
        ]))
    else:
        pass

async def query_chart(bot: Bot, event: MessageEvent, args: List[str], text: bool = False):

    try:
        match = regex.match(
            r"(绿|黄|红|紫|白|basic|advanced|expert|master|remaster|re:master)([\d]+)", 
            args[1], 
            regex.I
        )
        song_id = int(match.group()[1])
        chart_diff = diff_name_index[match.group()[0].lower()]
    except:
        return

    if not song_id in song_list:
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text("没有对应的歌曲呢。")
        ]))
        return

    song = song_list[song_id]

    if chart_diff + 1 > len(song.charts):
        await bot.send(event, Message([
            MessageSegment.reply(event.message_id),
            MessageSegment.text(f"这首歌曲没有 {diff_name[chart_diff]} 难度呢。")
        ]))
        return

    chart = song.charts[chart_diff]

    if text:
        await bot.send(event, Message([
            MessageSegment.image(image_to_bytes(await get_cover(song.song_id))),
            MessageSegment.text(f"\n{song_id}. {song.title}\n"),
            MessageSegment.text(f"谱面类型：" + ("DX" if song.dx_chart else "标准") + "\n"),
            MessageSegment.text(f"难度：{diff_name[chart_diff]} {chart.level_display}\n"),
            MessageSegment.text(f"定数：{chart.level:.1f}\n"),
            MessageSegment.text(f"谱师：{chart.charter}\n"),
            MessageSegment.text(f"Tap：{chart.tap_count}\n"),
            MessageSegment.text(f"Hold：{chart.hold_count}\n"),
            MessageSegment.text(f"Slide：{chart.slide_count}\n"),
            MessageSegment.text(f"Touch：{chart.touch_count}\n") if song.dx_chart else "",
            MessageSegment.text(f"Break：{chart.break_count}"),
        ]))
    else:
        pass