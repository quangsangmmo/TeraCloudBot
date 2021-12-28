import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import requests
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & ~filters.command(['start','users','broadcast','files','file','upload']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("<b>Vui lòng chờ...!</b>", quote = True)
    try:
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("<b>Đã xảy ra lỗi...!<b>")
        return
    converted_id = post_message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    # Link mặc định
    url = f"https://t.me/{client.username}?start={base64_string}"
    # Link olacity
    ola_link=requests.get(f"https://link.olacity.com/api/?api=46e2243ee2307a5d62bd7afa560150fec8f9d05d&url={url}").json()['shortenedUrl']
    # Link1s
    link = requests.get(f"https://link1s.com/api?api=9e9c26d7a2a2759289d9f95c84931a0471da7243&url={ola_link}").json()['shortenedUrl']
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await reply_text.edit(f"<b>✅ LƯU TRỮ THÀNH CÔNG \n\n🔗 Your URL : {link}</b>", reply_markup=reply_markup, disable_web_page_preview = True)
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID) & ~filters.edited)
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return
    converted_id = message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    urlfile = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={urlfile}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
