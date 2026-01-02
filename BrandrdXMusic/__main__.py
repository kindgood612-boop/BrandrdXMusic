import asyncio
import importlib
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from BrandrdXMusic import LOGGER, app, userbot
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # التحقق من وجود كود السيشن للحساب المساعد
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("لم يتم العثور على كود سيشن الحساب المساعد... جاري الخروج")
        exit()
    
    # تهيئة المشرفين وقوائم الحظر
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    
    # تشغيل البوت الأساسي
    await app.start()
    
    # استدعاء ملفات البلاجنز
    for all_module in ALL_MODULES:
        importlib.import_module(f"BrandrdXMusic.plugins.{all_module}")
        
    LOGGER("BrandrdXMusic.plugins").info("تم استدعاء ملفات البوت بنجاح")
    
    # تشغيل الحساب المساعد والمكالمات
    await userbot.start()
    await Hotty.start()
    
    # تم إزالة السطر القديم Hotty.decorators() لأنه غير موجود في الكود الجديد ويسبب خطأ
    
    # رسالة التشغيل النهائية (بالإيموجي والزخرفة)
    LOGGER("BrandrdXMusic").info(
        "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🤍 تم تشغيل البوت بنجاح\n"
        "🧚 المطور: @S_G0C7\n"
        "♥️ قناة السورس: https://t.me/SourceBoda\n"
        "💝 جروب الدعم: https://t.me/music0587\n"
        "💕 شكرا لاستخدامك سورس بودا\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    # إبقاء البوت يعمل
    await idle()
    
    # إيقاف التشغيل عند الإغلاق
    await app.stop()
    await userbot.stop()
    LOGGER("BrandrdXMusic").info("تم ايقاف البوت بنجاح")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
