from pyrogram import Client, filters
import asyncio
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
import requests
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('files'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Chuyển tiếp Post or Link đầu tiên từ kênh Database (có trích dẫn)\n<code>(Hết hạn sau 60s)</code>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("✖️ <b>Đã Sảy Ra Lỗi</b>\nPost or Link này không tồn tại hoặc không được chuyển tiếp từ kênh Database", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Chuyển tiếp Post or Link cuối cùng từ kênh Database (có trích dẫn)\n<code>(Hết hạn sau 60s)</code>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("✖️ <b>Đã Sảy Ra Lỗi</b>\nPost or Link này không tồn tại hoặc không được chuyển tiếp từ kênh Database", quote = True)
            continue
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>✅ LƯU TRỮ THÀNH CÔNG \n\n🔗 Your URL : {link}</b>\n", quote=True, reply_markup=reply_markup)