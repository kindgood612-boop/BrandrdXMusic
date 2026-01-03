from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config
from ..logging import LOGGER


class Hotty(Client):
    def __init__(self):
        LOGGER(__name__).info("جاري بدء تشغيل البوت...")

        super().__init__(
            name="BrandrdXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
        )

    async def start(self):
        await super().start()

        # التأكد من جلب بيانات البوت بشكل آمن
        me = self.me
        if not me:
            me = await self.get_me()

        self.id = me.id
        self.first_name = me.first_name or ""
        self.last_name = me.last_name or ""
        self.name = f"{self.first_name} {self.last_name}".strip()
        self.username = me.username
        self.mention = me.mention if me.mention else self.name

        # إرسال رسالة بدء التشغيل إلى مجموعة السجل
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=(
                    "<u><b>تم بدء تشغيل بوت الموسيقى بنجاح</b></u>\n\n"
                    f"الاسم الكامل: {self.name}\n"
                    f"المعرف: @{self.username}\n"
                    f"الايدي: <code>{self.id}</code>\n\n"
                    "البوت يعمل الآن وجاهز لاستقبال الأوامر وتشغيل الموسيقى بدون مشاكل."
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "فشل البوت في الوصول إلى مجموعة السجل. "
                "تأكد من إضافة البوت إلى المجموعة الصحيحة."
            )
        except Exception as ex:
            LOGGER(__name__).error(
                f"فشل إرسال رسالة السجل. السبب: {type(ex).__name__}"
            )

        # التحقق من أن البوت مشرف في مجموعة السجل
        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "البوت ليس مشرفًا في مجموعة السجل. "
                    "يرجى رفعه كمشرف لتجنب مشاكل مستقبلية."
                )
        except Exception:
            LOGGER(__name__).warning(
                "تعذر التحقق من صلاحيات البوت داخل مجموعة السجل."
            )

        LOGGER(__name__).info(f"تم بدء تشغيل بوت الميوزك باسم {self.name}")

    async def stop(self):
        LOGGER(__name__).info("جاري إيقاف البوت...")
        await super().stop()
