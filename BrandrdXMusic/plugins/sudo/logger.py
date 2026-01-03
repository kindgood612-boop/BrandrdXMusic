from pyrogram import filters

from BrandrdXMusic import app
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.core.database import add_off, add_on

# ==========================================================
# 1. تفعيل/تعطيل السجل (Logger)
# ==========================================================
# تم وضع الجمل الكاملة كأوامر لتعمل مباشرة
@app.on_message(filters.command(["تفعيل السجل", "تعطيل السجل", "logger"], prefixes=["", "/", "!", "."]) & SUDOERS)
async def logger(client, message):
    full_text = message.text.lower()

    # --- التفعيل ---
    # إذا كتب "تفعيل السجل" أو أمر logger ومعه كلمة enable
    if "تفعيل" in full_text or "enable" in full_text:
        await add_on(2)
        await message.reply_text("♥️ **تـم تـفـعـيـل سـجـل الـبـوت (Logger) بـنـجـاح.**")
        
    # --- التعطيل ---
    # إذا كتب "تعطيل السجل" أو أمر logger ومعه كلمة disable
    elif "تعطيل" in full_text or "disable" in full_text:
        await add_off(2)
        await message.reply_text("💕 **تـم تـعـطـيـل سـجـل الـبـوت (Logger) بـنـجـاح.**")
        
    # --- إذا كتب "logger" فقط بدون تحديد ---
    else:
        await message.reply_text(
            "🥀 **طـريـقـة الاسـتـخـدام :**\n\n"
            "فـقـط اكـتـب الأمـر مـبـاشـرة:\n"
            "• **تفعيل السجل**\n"
            "• **تعطيل السجل**"
        )


# ==========================================================
# 2. سحب ملف السجلات
# ==========================================================
# تم دمج "ملف السجل" كأمر واحد
@app.on_message(filters.command(["logs", "ملف السجل", "السجلات"], prefixes=["", "/", "!", "."]) & SUDOERS)
async def get_cookies_logs(client, message):
    try:
        await message.reply_document(
            document="cookies/logs.csv",
            caption="🧚 **تـفـضـل مـلـف سـجـلات الـبـوت (Logs/Cookies)...**"
        )
    except:
        await message.reply_text("🥀 **عـذراً، لـم يـتـم الـعـثـور عـلـى مـلـف الـسـجـلات.**")
