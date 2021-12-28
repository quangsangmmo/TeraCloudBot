from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests
@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = """<b>
⟩⟩ Tạo Bởi <a href='https://fb.com/sang1900'>Nguyễn Sáng</a>
⟩⟩ Phiên Bản : <code>Premium</code>
ℹ️ THÔNG TIN CHI TIẾT :</b>
- Chức năng : lưu trữ dữ liệu (tin nhắn, file, hình ảnh, video...)
- Kéo member : OFF
- Trả lời tự động : ON
- Lưu trữ không short link : 15k/tháng
(Tạo BOT lưu trữ tự quản lý liên hệ <a href='https://fb.com/sang1900'>Nguyễn Sáng</a>)""",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("❌ Đóng", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass