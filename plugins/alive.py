import asyncio
from time import time
from datetime import datetime
from modules.helpers.filters import command
from modules.helpers.command import commandpro
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)
    
   

@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/95d0ad6ac9784ab56df7b.jpg",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
😇𝗧𝗛𝗜𝗦 𝗜𝗦 𝗧𝗛𝗘 𝗕𝗘𝗦𝗧 𝗠𝗨𝗦𝗜𝗖 𝗕𝗢𝗧 𝗠𝗔𝗗𝗘 𝗕𝗬 𝗧𝗢𝗫𝗜𝗖 𝗗𝗔𝗡𝗚𝗘𝗥𝗢𝗨𝗦𝗙𝗜𝗚𝗛𝗧𝗘𝗥
┏━━━━━━━━━━━━━━━━━┓
┣★ 𝐎𝐰𝐧𝐞𝐫: [𝐓𝐨𝐱𝐢𝐜](https://t.me/wtf_realtoxic)
┣★ 𝐂𝐡𝐚𝐧𝐧𝐞𝐥:[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/Dangerousfighterchannel)
┣★ 𝐆𝐫𝐨𝐮𝐩: [𝐂𝐡𝐚𝐭𝐭𝐢𝐧𝐠](https://t.me/Dangerouschatting)
┗━━━━━━━━━━━━━━━━━┛

𝗜𝗳 𝘆𝗼𝘂 𝗵𝗮𝘃𝗲 𝗮𝗻𝘆 𝗱𝗼𝘂𝗯𝘁 𝗸𝗲𝗲𝗽 𝗰𝗼𝗺𝘁𝗮𝗰𝘁 𝘁𝗼 𝗼𝘄𝗻𝗲𝗿 
       𝗧𝗼𝘅𝗶𝗰 :-(https://t.me/wtf_realtoxic)😇😍...
━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝗗𝗮𝗻𝗴𝗲𝗿𝗼𝘂𝘀𝗰𝗵𝗮𝗻𝗻𝗲𝗹", url=f"https://t.me/Dangerousfighterchannel")
                ]
                
           ]
        ),
    )
    
    
@Client.on_message(commandpro(["/start", "/alive", "#Toxic"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://te.legra.ph/file/c6e1041c6c9a12913f57a.png",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "𝗗𝗮𝗻𝗴𝗲𝗿𝗼𝘂𝘀𝗰𝗵𝗮𝘁𝘁𝗶𝗻𝗴", url=f"https://t.me/Dangerouschatting")
                ]
            ]
        ),
    )


@Client.on_message(commandpro(["repo", "#repo", "@repo", "/repo", "source"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/95d0ad6ac9784ab56df7b.jpg",
        caption=f"""""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💥 ᴄʟɪᴄᴋ ᴍᴇ ᴛᴏ ɢᴇᴛ ʀᴇᴘᴏ 💞", url=f"https://t.me/wtf_realtoxic")
                ]
            ]
        ),
    )
