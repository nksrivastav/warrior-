from pyrogram import idle
from pyrogram import Client as Bot
from modules import bot
from modules.clientbot import run
from modules.config import API_ID, API_HASH, BOT_TOKEN



bot.start()
run()
idle()
