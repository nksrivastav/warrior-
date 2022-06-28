# Aditya Halder // @AdityaHalder
# Toxic𝐌𝐮𝐬𝐢𝐜 // @wtf_realtoxic
import os
import aiofiles
import aiohttp
import ffmpeg
import random
import requests
from os import path
from modules import bot
from asyncio.queues import QueueEmpty
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from modules.cache.admins import set
from modules.clientbot import clientbot, queues
from modules.clientbot.clientbot import client as USER
from modules.helpers.admins import get_administrators
from youtube_search import YoutubeSearch
from modules import converter
from modules.downloaders import youtube
from modules.config import DURATION_LIMIT, que, SUDO_USERS
from modules.cache.admins import admins as a
from modules.helpers.filters import command, other_filters
from modules.helpers.command import commandpro
from modules.helpers.decorators import errors, authorized_users_only
from modules.database.dbchat import (get_served_chats, is_served_chat, add_served_chat)
from modules.helpers.errors import DurationLimitError
from modules.helpers.gets import get_url, get_file_name
from PIL import Image, ImageFont, ImageDraw
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputStream
from pytgcalls.types.input_stream import InputAudioStream

# plus
chat_id = None
useer = "NaN"

themes = [
    "bgreen",
    "blue",
    "colorfull",
    "dgreen",
    "hgreen",
    "lgreen",
    "lyellow",
    "orange",
    "pink",
    "purple",
    "rainbow",
    "red",
    "sky",
    "thumbnail",
    "yellow",
]

def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(filename)


# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))


async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    theme = random.choice(themes)
    image1 = Image.open("./background.png")
    image2 = Image.open(f"resource/{theme}.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("resource/font.otf", 32)
    draw.text((190, 550), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((190, 590), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text(
        (190, 670),
        f"Powered By: Toxic (@wtf_realtoxic)",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    commandpro(["play", "/play", "!play", ".play", "ply", "@", "#"])
    & filters.group
    & ~filters.edited
    & ~filters.forwarded
    & ~filters.via_bot
)
async def play(_, message: Message):
    global que
    global useer
    await message.delete()

    lel = await message.reply("**🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 ...**")

    if not await is_served_chat(message.chat.id):
        await lel.edit(f"**🥀 𝐒𝐨𝐫𝐫𝐲 𝐓𝐡𝐢𝐬 🌺 𝐌𝐮𝐬𝐢𝐜 𝐑𝐨𝐛𝐨𝐭\n𝐎𝐧𝐥𝐲 𝐅𝐨𝐫 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐔𝐬𝐞𝐫𝐬 ✨...\n\n💐 𝐈𝐟 𝐘𝐨𝐮 ❥︎𝐖𝐚𝐧𝐭 🌸 𝐭𝐨 𝐀𝐝𝐝 𝐢𝐧\n𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 𝐓𝐡𝐞𝐧 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 🌷\n❥︎ 𝐓𝐨 ➪ [Toxic](https://t.me/wtf_realtoxic) ...**", disable_web_page_preview=True)
        return await bot.leave_chat(message.chat.id)  
    if message.sender_chat:
        return await lel.edit("**🥀 𝐏𝐥𝐞𝐚𝐬𝐞 𝐃𝐨𝐧'𝐭 𝐔𝐬𝐞 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐅𝐨𝐫 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 ✨ ...**")  
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "⏤͟͟͞❥͜͡𝄟⃟𝗧𝗼𝘅𝗶𝗰🕊️⃝‌ٖٖٖٖ ‌ٖٖٖٖٖ🦋𝐌𝐮𝐬𝐢𝐜𝄟⃟🎸"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "**𝗣𝗲𝗵𝗹𝗲 𝗮𝗱𝗺𝗶𝗻 𝘁𝗼𝗵 𝗯𝗮𝗻𝗮𝗼...**")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "** 𝗦𝗼𝗻𝗴 𝗯𝗮𝗷𝗮𝗻𝗲 𝗸𝗲 𝗹𝗶𝘆𝗲 𝗿𝗲𝗮𝗱𝘆 𝗵𝘂 ...**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"** 𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗸𝗼 𝗺𝗮𝗻𝘂𝗮𝗹𝗹𝘆 𝗮𝗱𝗱 𝗸𝗮𝗿𝗼 𝘆𝗮 𝗼𝗻𝘄𝗲𝗿 𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗸𝗮𝗿𝗼ː [Toxic](https://t.me/wtf_realtoxic) ✨ ...**")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"** 𝗔𝘀𝘀𝗶𝘀𝘁𝗮𝗻𝘁 𝗸𝗼 𝗺𝗮𝗻𝘂𝗮𝗹𝗹𝘆 𝗮𝗱𝗱 𝗸𝗮𝗿𝗼 𝘆𝗮 𝗼𝗻𝘄𝗲𝗿 𝘀𝗲 𝗰𝗼𝗻𝘁𝗮𝗰𝘁 𝗸𝗮𝗿𝗼ː [Toxic](https://t.me/wtf_realtoxic) ✨ ...**")
        return
    
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"**💥 𝐏𝐥𝐚𝐲 🔊 𝐌𝐮𝐬𝐢𝐜 💿 𝐋𝐞𝐬𝐬 ⚡️\n🤟 𝐓𝐡𝐚𝐧⚡️ {DURATION_LIMIT} 💞 𝐌𝐢𝐧𝐮𝐭𝐞 ...**"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/95d0ad6ac9784ab56df7b.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝗚𝗿𝗼𝘂𝗽",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝗚𝗿𝗼𝘂𝗽",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/95d0ad6ac9784ab56df7b.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝗚𝗿𝗼𝘂𝗽",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**💥 𝐏𝐥𝐚𝐲 🔊 𝐌𝐮𝐬𝐢𝐜 💿 𝐋𝐞𝐬𝐬 ⚡️\n🤟 𝐓𝐡𝐚𝐧⚡️ {DURATION_LIMIT} 💞 𝐌𝐢𝐧𝐮𝐭𝐞 ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit(
                "**🤖 𝐆𝐢𝐯𝐞 🙃 𝐌𝐮𝐬𝐢𝐜 💿 𝐍𝐚𝐦𝐞 😍\n💞 𝐓𝐨 🔊 𝐏𝐥𝐚𝐲 🥀 𝐒𝐨𝐧𝐠 🌷...**"
            )
        await lel.edit("**🔄 𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 ...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"thumb{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(":")
            for i in range(len(dur_arr) - 1, -1, -1):
                dur += int(dur_arr[i]) * secmul
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**🔊 𝐌𝐮𝐬𝐢𝐜 😕 𝐍𝐨𝐭 📵 𝐅𝐨𝐮𝐧𝐝❗️\n💞 𝐓𝐫𝐲 ♨️ 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 🌷...**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="𝗚𝗿𝗼𝘂𝗽",
                            url=f"https://t.me/Dangerouschatting")

                ]
            ]
        )

        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"**💥 𝐏𝐥𝐚𝐲 🔊 𝐌𝐮𝐬𝐢𝐜 💿 𝐋𝐞𝐬𝐬 ⚡️\n🤟 𝐓𝐡𝐚𝐧⚡️ {DURATION_LIMIT} 💞 𝐌𝐢𝐧𝐮𝐭𝐞 ...**"
            )
            return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        await message.reply_photo(
            photo="final.png",
            caption="💥 𝗧𝗼𝘅𝗶𝗰🤞𝐌𝐮𝐬𝐢𝐜 💿 𝐐𝐮𝐞𝐮𝐞𝐝❗️\n🔊 𝐀𝐭 💞 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 » `{}` 🌷 ...**".format(position),
            reply_markup=keyboard,
        )
    else:
        await clientbot.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )

        await message.reply_photo(
            photo="final.png",
            reply_markup=keyboard,
            caption="**💥 𝗧𝗼𝘅𝗶𝗰🤞𝐌𝐮𝐬𝐢𝐜 🎸 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 💞\n🔊 𝐂𝐮𝐫𝐫𝐞𝐧𝐭 😍 𝐒𝐨𝐧𝐠 🥀 ...**".format(),
           )

    os.remove("final.png")
    return await lel.delete()
    
    
@Client.on_message(commandpro(["pause", "/pause", "!pause", ".pause", "pse"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await message.delete()
    await clientbot.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("**𝐏𝐚𝐮𝐬𝐞𝐝 🌷 ...**")


@Client.on_message(commandpro(["resume", "/resume", "!resume", ".resume", "rsm"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await message.delete()
    await clientbot.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("**𝐑𝐞𝐬𝐮𝐦𝐞𝐝 🌷 ...**")



@Client.on_message(commandpro(["skip", "/skip", "!skip", ".skip", "skp"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    await message.delete()
    ACTV_CALLS = []
    chat_id = message.chat.id
    for x in clientbot.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALLS:
        await message.reply_text("**𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 🌷 ...**")
    else:
        queues.task_done(chat_id)
        
        if queues.is_empty(chat_id):
            await clientbot.pytgcalls.leave_group_call(chat_id)
            await message.reply_text("**🥀 𝐄𝐦𝐩𝐭𝐲 𝐐𝐮𝐞𝐮𝐞, 𝐋𝐞𝐚𝐯𝐢𝐧𝐠 𝐕𝐂 ✨...**")
        else:
            await message.reply_text("**𝐒𝐤𝐢𝐩𝐩𝐞𝐝 🌷 ...**")
            await clientbot.pytgcalls.change_stream(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        clientbot.queues.get(chat_id)["file"],
                    ),
                ),
            )



@Client.on_message(commandpro(["stop", "end", "/stop", "/end", "!stop", "!end", ".stop", ".end", "stp"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    await message.delete()
    try:
        clientbot.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await clientbot.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("**𝐒𝐭𝐨𝐩𝐩𝐞𝐝 🌷 ...**")


@Client.on_message(commandpro(["reload", "/reload", "!reload", ".reload", "rld"]) & other_filters)
@errors
@authorized_users_only
async def update_admin(client, message):
    global a
    await message.delete()
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    a[message.chat.id] = new_admins
    await message.reply_text("**𝐑𝐞𝐥𝐨𝐚𝐝𝐞𝐝 🌷 ...**")
