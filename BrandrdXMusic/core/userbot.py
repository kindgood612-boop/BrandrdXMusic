import asyncio
from pyrogram import Client
import config
from ..logging import LOGGER

assistants = []
assistantids = []


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

    async def start(self):
        LOGGER(__name__).info("جاري تشغيل الحسابات المساعدة...")

        # =====================
        # الحساب الأول
        # =====================
        if config.STRING1:
            try:
                await self.one.start()
                try:
                    await self.one.join_chat(config.LOGGER_ID)
                    await self.one.send_message(
                        config.LOGGER_ID,
                        "تم تشغيل الحساب المساعد الأول"
                    )
                except Exception:
                    LOGGER(__name__).warning(
                        "الحساب المساعد 1 لم يتمكن من دخول جروب السجل"
                    )

                assistants.append(1)

                me = await self.one.get_me()
                self.one.id = me.id
                self.one.name = me.mention
                self.one.username = me.username
                assistantids.append(me.id)

                LOGGER(__name__).info(
                    f"تم تشغيل المساعد الأول | {self.one.name}"
                )
            except Exception as e:
                LOGGER(__name__).error(
                    f"فشل تشغيل الحساب المساعد الأول | {e}"
                )

        # =====================
        # الحساب الثاني
        # =====================
        if config.STRING2:
            try:
                await self.two.start()
                try:
                    await self.two.join_chat(config.LOGGER_ID)
                    await self.two.send_message(
                        config.LOGGER_ID,
                        "تم تشغيل الحساب المساعد الثاني"
                    )
                except Exception:
                    LOGGER(__name__).warning(
                        "الحساب المساعد 2 لم يتمكن من دخول جروب السجل"
                    )

                assistants.append(2)

                me = await self.two.get_me()
                self.two.id = me.id
                self.two.name = me.mention
                self.two.username = me.username
                assistantids.append(me.id)

                LOGGER(__name__).info(
                    f"تم تشغيل المساعد الثاني | {self.two.name}"
                )
            except Exception as e:
                LOGGER(__name__).error(
                    f"فشل تشغيل الحساب المساعد الثاني | {e}"
                )

        # =====================
        # الحساب الثالث
        # =====================
        if config.STRING3:
            try:
                await self.three.start()
                try:
                    await self.three.join_chat(config.LOGGER_ID)
                    await self.three.send_message(
                        config.LOGGER_ID,
                        "تم تشغيل الحساب المساعد الثالث"
                    )
                except Exception:
                    LOGGER(__name__).warning(
                        "الحساب المساعد 3 لم يتمكن من دخول جروب السجل"
                    )

                assistants.append(3)

                me = await self.three.get_me()
                self.three.id = me.id
                self.three.name = me.mention
                self.three.username = me.username
                assistantids.append(me.id)

                LOGGER(__name__).info(
                    f"تم تشغيل المساعد الثالث | {self.three.name}"
                )
            except Exception as e:
                LOGGER(__name__).error(
                    f"فشل تشغيل الحساب المساعد الثالث | {e}"
                )

        # =====================
        # الحساب الرابع
        # =====================
        if config.STRING4:
            try:
                await self.four.start()
                try:
                    await self.four.join_chat(config.LOGGER_ID)
                    await self.four.send_message(
                        config.LOGGER_ID,
                        "تم تشغيل الحساب المساعد الرابع"
                    )
                except Exception:
                    LOGGER(__name__).warning(
                        "الحساب المساعد 4 لم يتمكن من دخول جروب السجل"
                    )

                assistants.append(4)

                me = await self.four.get_me()
                self.four.id = me.id
                self.four.name = me.mention
                self.four.username = me.username
                assistantids.append(me.id)

                LOGGER(__name__).info(
                    f"تم تشغيل المساعد الرابع | {self.four.name}"
                )
            except Exception as e:
                LOGGER(__name__).error(
                    f"فشل تشغيل الحساب المساعد الرابع | {e}"
                )

        # =====================
        # الحساب الخامس
        # =====================
        if config.STRING5:
            try:
                await self.five.start()
                try:
                    await self.five.join_chat(config.LOGGER_ID)
                    await self.five.send_message(
                        config.LOGGER_ID,
                        "تم تشغيل الحساب المساعد الخامس"
                    )
                except Exception:
                    LOGGER(__name__).warning(
                        "الحساب المساعد 5 لم يتمكن من دخول جروب السجل"
                    )

                assistants.append(5)

                me = await self.five.get_me()
                self.five.id = me.id
                self.five.name = me.mention
                self.five.username = me.username
                assistantids.append(me.id)

                LOGGER(__name__).info(
                    f"تم تشغيل المساعد الخامس | {self.five.name}"
                )
            except Exception as e:
                LOGGER(__name__).error(
                    f"فشل تشغيل الحساب المساعد الخامس | {e}"
                )

    async def stop(self):
        LOGGER(__name__).info("جاري إيقاف الحسابات المساعدة...")

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
