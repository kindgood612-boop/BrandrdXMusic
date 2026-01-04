import asyncio
import importlib
from pyrogram import idle, filters
import pyrogram.errors

# ==== PATCH for pyrogram GroupcallForbidden ====
if not hasattr(pyrogram.errors, "GroupcallForbidden"):
    class GroupcallForbidden(Exception):
        pass
    pyrogram.errors.GroupcallForbidden = GroupcallForbidden
# =============================================

import config
from BrandrdXMusic import LOGGER, app, userbot
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import sudo
from BrandrdXMusic.plugins import ALL_MODULES
from BrandrdXMusic.core.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    # =======================
    # Check assistant sessions
    # =======================
    if not any([
        config.STRING1,
        config.STRING2,
        config.STRING3,
        config.STRING4,
        config.STRING5,
    ]):
        LOGGER(__name__).error("❌ لم يتم العثور على أي كود سيشن للحسابات المساعدة")
        return

    # =======================
    # Load sudo & bans
    # =======================
    await sudo()

    try:
        for user_id in await get_gbanned():
            BANNED_USERS.add(int(user_id))
        for user_id in await get_banned_users():
            BANNED_USERS.add(int(user_id))
    except Exception as e:
        LOGGER(__name__).warning(f"Banned users load skipped: {e}")

    # =======================
    # 🚨 أمر تجربة مباشر (TEST COMMAND)
    # =======================
    # هذا الأمر موجود داخل ملف التشغيل مباشرة لضمان أن البوت يستجيب
    @app.on_message(filters.command(["test", "تست", "alive"], prefixes=["/", "!", ".", ""]))
    async def test_command(client, message):
        await message.reply_text(
            "✅ **البوت متصل وشغال 100% يا حب!**\n"
            "المشكلة كانت في ترتيب تحميل الملفات، دلوقتي كله تمام."
        )

    # =======================
    # ✅ LOAD PLUGINS FIRST (قبل التشغيل)
    # =======================
    # الترتيب ده مهم جداً عشان الأوامر تشتغل
    for module_name in ALL_MODULES:
        try:
            importlib.import_module(f"BrandrdXMusic.plugins.{module_name}")
        except Exception as e:
            LOGGER("BrandrdXMusic.plugins").error(
                f"❌ خطأ في تحميل البلجن {module_name}: {e}"
            )

    LOGGER("BrandrdXMusic.plugins").info("✅ تم استدعاء ملفات البوت بنجاح")

    # =======================
    # ✅ START CLIENTS
    # =======================
    await app.start()       
    await userbot.start()   
    await Hotty.start()     
    
    try:
        await Hotty.decorators()
    except Exception as e:
        LOGGER("CallDecorators").warning(f"Decorators warning: {e}")

    # =======================
    # Startup message
    # =======================
    LOGGER("BrandrdXMusic").info(
        "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🤍 تم تشغيل البوت بنجاح\n"
        "🧚 المطور: @S_G0C7\n"
        "♥️ قناة السورس: https://t.me/SourceBoda\n"
        "💝 جروب الدعم: https://t.me/music0587\n"
        "💕 شكرا لاستخدامك سورس بودا\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )

    # =======================
    # Idle
    # =======================
    await idle()

    # =======================
    # Graceful shutdown (SAFE MODE)
    # =======================
    LOGGER("BrandrdXMusic").info("🛑 جاري إيقاف البوت...")
    
    try:
        await Hotty.one.stop()
    except: pass
    
    try:
        await userbot.stop()
    except: pass
    
    try:
        await app.stop()
    except: pass


if __name__ == "__main__":
    asyncio.run(init())
