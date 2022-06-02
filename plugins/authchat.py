from pyrogram import filters, Client
from pyrogram.types import Message

from modules import bot as app
from modules.helpers.decorators import errors, sudo_users_only
from modules.helpers.command import commandpro
from modules.database.dbchat import (get_served_chats, is_served_chat, add_served_chat, remove_served_chat)  


@app.on_message(commandpro(["add"]))
@errors
@sudo_users_only
async def auth_chat_func(_, message: Message):
    await message.delete()
    if len(message.command) != 2:
        return await message.reply_text("**🥀 𝐆𝐢𝐯𝐞 𝐂𝐡𝐚𝐭 𝐈𝐃 𝐅𝐨𝐫 𝐀𝐥𝐥𝐨𝐰 ✨ ...**")
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
        await message.reply_text("✅ 𝐂𝐡𝐚𝐭 𝐀𝐝𝐝𝐞𝐝 𝐓𝐨 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞.")
    else:
        await message.reply_text("✅ 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐝𝐝𝐞𝐝.")


@app.on_message(commandpro(["del"]))
@errors
@sudo_users_only
async def unauth_chat_func(_, message: Message):
    await message.delete()
    if len(message.command) != 2:
        return await message.reply_text(
            "**🥀 𝐆𝐢𝐯𝐞 𝐂𝐡𝐚𝐭 𝐈𝐃 𝐅𝐨𝐫 𝐃𝐢𝐬𝐀𝐥𝐥𝐨𝐰 ✨ ...**"
        )
    chat_id = int(message.text.strip().split()[1])
    if not await is_served_chat(chat_id):
        await message.reply_text("❌ 𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐍𝐨𝐭 𝐢𝐧 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞.")
        return
    try:
        await remove_served_chat(chat_id)
        await message.reply_text("❌ 𝐂𝐡𝐚𝐭 𝐑𝐞𝐦𝐨𝐯𝐞𝐝 𝐅𝐫𝐨𝐦 𝐃𝐚𝐭𝐚𝐛𝐚𝐬𝐞.")
        return
    except Exception as e:
      await message.reply_text(f"error: `{e}`")


@app.on_message(commandpro("chats"))
@errors
@sudo_users_only
async def blacklisted_chats_func(_, message: Message):
    await message.delete()
    served_chats = []
    text = "📡 **𝐀𝐥𝐥𝐨𝐰𝐞𝐝 𝐂𝐡𝐚𝐭𝐬:**\n\n"
    try:
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"error: `{e}`")
        return
    count = 0
    for served_chat in served_chats:
        
        try:
            title = (await app.get_chat(served_chat)).title
        except Exception:
            title = "Private"
        count += 1
        text += f"**{count}. {title}** [`{served_chat}`]\n"
    if not text:
        await message.reply_text("❌ **𝐍𝐨 𝐀𝐥𝐥𝐨𝐰𝐞𝐝 𝐂𝐡𝐚𝐭𝐬**")  
    else:
        await message.reply_text(text) 
