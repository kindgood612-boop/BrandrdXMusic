import asyncio
from pyrogram import Client

import config
from BrandrdXMusic.logging import LOGGER

# =====================
# Globals
# =====================

assistants = []
assistantids = []


# =====================
# Userbot Class
# =====================

class Userbot:
    def __init__(self):
        self.one = Client(
            name="BrandrdXMusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )

        self.two = Client(
            name="BrandrdXMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )

        self.three = Client(
            name="BrandrdXMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )

        self.four = Client(
            name="BrandrdXMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )

        self.five = Client(
            name="BrandrdXMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )

    # =====================
    # Start Assistants
    # =====================

    async def start(self):
        LOGGER(__name__).info("🚀 جاري تشغيل الحسابات المساعدة...")

        # ========= Assistant 1 =========
        if config.STRING1:
            try:
                await self.one.start()
                me = await self.one.get_me()

                self.one.id = me.id
                self.one.name = me.mention
                self.one.username = me.username

                if me.id not in assistantids:
                    assistants.append(1)
                    assistantids.append(me.id)

                try:
                    await self.one.join_chat(config.LOGGER_ID)
                    await self.one.send_message(
                        config.LOGGER_ID,
                        "✅ تم تشغيل الحساب المساعد الأول"
                    )
                except Exception:
                    LOGGER(__name__).warning("⚠️ المساعد 1 لم يدخل جروب السجل")

                LOGGER(__name__).info(f"✅ المساعد الأول شغال | {self.one.name}")

            except Exception as e:
                LOGGER(__name__).error(f"❌ فشل تشغيل المساعد الأول | {e}")

        # ========= Assistant 2 =========
        if config.STRING2:
            try:
                await self.two.start()
                me = await self.two.get_me()

                self.two.id = me.id
                self.two.name = me.mention
                self.two.username = me.username

                if me.id not in assistantids:
                    assistants.append(2)
                    assistantids.append(me.id)

                try:
                    await self.two.join_chat(config.LOGGER_ID)
                    await self.two.send_message(
                        config.LOGGER_ID,
                        "✅ تم تشغيل الحساب المساعد الثاني"
                    )
                except Exception:
                    LOGGER(__name__).warning("⚠️ المساعد 2 لم يدخل جروب السجل")

                LOGGER(__name__).info(f"✅ المساعد الثاني شغال | {self.two.name}")

            except Exception as e:
                LOGGER(__name__).error(f"❌ فشل تشغيل المساعد الثاني | {e}")

        # ========= Assistant 3 =========
        if config.STRING3:
            try:
                await self.three.start()
                me = await self.three.get_me()

                self.three.id = me.id
                self.three.name = me.mention
                self.three.username = me.username

                if me.id not in assistantids:
                    assistants.append(3)
                    assistantids.append(me.id)

                try:
                    await self.three.join_chat(config.LOGGER_ID)
                    await self.three.send_message(
                        config.LOGGER_ID,
                        "✅ تم تشغيل الحساب المساعد الثالث"
                    )
                except Exception:
                    LOGGER(__name__).warning("⚠️ المساعد 3 لم يدخل جروب السجل")

                LOGGER(__name__).info(f"✅ المساعد الثالث شغال | {self.three.name}")

            except Exception as e:
                LOGGER(__name__).error(f"❌ فشل تشغيل المساعد الثالث | {e}")

        # ========= Assistant 4 =========
        if config.STRING4:
            try:
                await self.four.start()
                me = await self.four.get_me()

                self.four.id = me.id
                self.four.name = me.mention
                self.four.username = me.username

                if me.id not in assistantids:
                    assistants.append(4)
                    assistantids.append(me.id)

                try:
                    await self.four.join_chat(config.LOGGER_ID)
                    await self.four.send_message(
                        config.LOGGER_ID,
                        "✅ تم تشغيل الحساب المساعد الرابع"
                    )
                except Exception:
                    LOGGER(__name__).warning("⚠️ المساعد 4 لم يدخل جروب السجل")

                LOGGER(__name__).info(f"✅ المساعد الرابع شغال | {self.four.name}")

            except Exception as e:
                LOGGER(__name__).error(f"❌ فشل تشغيل المساعد الرابع | {e}")

        # ========= Assistant 5 =========
        if config.STRING5:
            try:
                await self.five.start()
                me = await self.five.get_me()

                self.five.id = me.id
                self.five.name = me.mention
                self.five.username = me.username

                if me.id not in assistantids:
                    assistants.append(5)
                    assistantids.append(me.id)

                try:
                    await self.five.join_chat(config.LOGGER_ID)
                    await self.five.send_message(
                        config.LOGGER_ID,
                        "✅ تم تشغيل الحساب المساعد الخامس"
                    )
                except Exception:
                    LOGGER(__name__).warning("⚠️ المساعد 5 لم يدخل جروب السجل")

                LOGGER(__name__).info(f"✅ المساعد الخامس شغال | {self.five.name}")

            except Exception as e:
                LOGGER(__name__).error(f"❌ فشل تشغيل المساعد الخامس | {e}")

    # =====================
    # Stop Assistants
    # =====================

    async def stop(self):
        LOGGER(__name__).info("🛑 جاري إيقاف الحسابات المساعدة...")

        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except Exception:
            pass
