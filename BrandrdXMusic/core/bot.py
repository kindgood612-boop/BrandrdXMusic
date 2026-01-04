from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.errors import FloodWait
import asyncio

import config
from BrandrdXMusic.logging import LOGGER


class Hotty(Client):
    def __init__(self):
        LOGGER(__name__).info("🚀 جاري بدء تشغيل البوت...")

        super().__init__(
            name="BrandrdXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()

        # ===== جلب بيانات البوت بشكل آمن =====
        me = await self.get_me()
        self.id = me.id
        self.first_name = me.first_name or ""
        self.last_name = me.last_name or ""
        self.name = f"{self.first_name} {self.last_name}".strip()
        self.username = me.username
        self.mention = me.mention if me.mention else self.name

        # ===== إرسال رسالة اللوج (غير قاتلة) =====
        if config.LOGGER_ID:
            try:
                await self.send_message(
                    chat_id=config.LOGGER_ID,
                    text=(
                        "<u><b>» تم تشغيل بوت الميوزك بنجاح</b></u>\n\n"
                        f"🆔 الايدي: <code>{self.id}</code>\n"
                        f"🤖 الاسم: {self.name}\n"
                        f"🔗 اليوزر: @{self.username}"
                    ),
                )

            except FloodWait as e:
                LOGGER(__name__).warning(
                    f"FloodWait أثناء إرسال رسالة اللوج، انتظار {e.value} ثانية"
                )
                await asyncio.sleep(e.value)

            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error(
                    "❌ البوت فشل في الوصول لجروب/قناة اللوج، "
                    "تأكد إن البوت مضاف."
                )

            except Exception as ex:
                LOGGER(__name__).error(
                    f"❌ فشل إرسال رسالة اللوج. السبب: {type(ex).__name__}"
                )

            # ===== التحقق من صلاحيات الأدمن (تحذير فقط) =====
            try:
                member = await self.get_chat_member(config.LOGGER_ID, self.id)
                if member.status != ChatMemberStatus.ADMINISTRATOR:
                    LOGGER(__name__).warning(
                        "⚠️ البوت ليس مشرفًا في جروب اللوج."
                    )
            except Exception:
                LOGGER(__name__).warning(
                    "⚠️ تعذر التحقق من صلاحيات البوت داخل جروب اللوج."
                )

        LOGGER(__name__).info(f"✅ تم تشغيل بوت الميوزك باسم {self.name}")

    async def stop(self):
        LOGGER(__name__).info("🛑 جاري إيقاف البوت...")
        await super().stop()
