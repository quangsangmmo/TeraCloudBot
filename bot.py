import pyromod.listen
from pyrogram import Client
import sys

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID

class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()

        if FORCE_SUB_CHANNEL:
            try:
                link = await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot không thể xuất liên kết Mời từ Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Vui lòng kiểm tra kỹ giá trị FORCE_SUB_CHANNEL và đảm bảo Bot là Quản trị viên trong kênh với tính năng Mời người dùng thông qua Quyền liên kết, Giá trị kênh phụ hiện tại: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Inbox https://fb.com/sang1900")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Đảm bảo bot của Sure là Quản trị viên trong Kênh DB và kiểm tra kỹ Giá trị CHANNEL_ID, Giá trị hiện tại {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Inbox https://fb.com/sang1900")
            sys.exit()

        self.set_parse_mode("html")
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by Nguyễn Văn Sáng\nhttps://fb.com/sang1900")
        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
