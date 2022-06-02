from pyrogram import Client as Bot
from modules.config import API_ID, API_HASH, BOT_TOKEN
from modules.clientbot.clientbot import client
    
bot = Bot(
    ":kaal:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)
