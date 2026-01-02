import os
import inspect
from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from config import OWNER_ID
from BrandrdXMusic.utils.database import (
    is_maintenance,
    maintenance_off,
    maintenance_on,
    is_on_off,
    add_on,
    add_off,
)

# --- دالة ذكية لمعالجة أوامر قاعدة البيانات (Sync/Async) ---
async def safe_db_call(func, *args, **kwargs):
    """
    تقوم هذه الدالة بتنفيذ أوامر قاعدة البيانات سواء كانت تتطلب await أم لا.
    تحل مشكلة TypeError بشكل نهائي.
    """
    try:
        # المحاولة الأولى: نعتبرها async ونستخدم await
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            # إذا لم تكن async، ننفذها مباشرة
            result = func(*args, **kwargs)
            # إذا أرجعت coroutine (في بعض الحالات النادرة)، ننتظره
            if inspect.isawaitable(result):
                return await result
            return result
    except TypeError:
        # محاولة احتياطية: التشغيل المباشر في حال فشل الفحص
        return func(*args, **kwargs)

# -----------------------------------------------------------

# 1. الحارس (Maintenance Check)
@app.on_message(filters.all & ~filters.user(OWNER_ID), group=-1)
async def maintenance_check(client, message: Message):
    try:
        if not message.text:
            return
            
        # استخدام الدالة الذكية للفحص
        is_maint = await safe_db_call(is_maintenance)
        
        if is_maint:
            await message.reply_text(
                "**الـبـوت فـي وضـع الـصـيـانـة حـالـيـاً**\n\nنـحـن نـعـمـل عـلـى تـحـديـث الـبـوت، يـرجـى الـمـحـاولـة لاحـقـاً."
            )
            message.stop_propagation()
    except Exception:
        pass


# 2. أوامر الصيانة (للمطور فقط)
@app.on_message(filters.command(["maintenance", "الصيانة"], prefixes=["/", "!", ".", ""]) & filters.user(OWNER_ID))
async def maintenance(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**طـريـقـة اسـتـخـدام وضـع الـصـيـانـة:**\n\n"
            "• لـتـفـعـيـل الـصـيـانـة ارسـل: الـصـيـانـة تـفـعـيـل\n"
            "• لـتـعـطـيـل الـصـيـانـة ارسـل: الـصـيـانـة تـعـطـيـل"
        )
        
    state = message.text.split(None, 1)[1].strip().lower()
    
    try:
        if state in ["enable", "تفعيل", "on"]:
            if await safe_db_call(is_maintenance):
                await message.reply_text("وضـع الـصـيـانـة مـفـعّـل بـالـفـعـل!")
            else:
                await safe_db_call(maintenance_on)
                await message.reply_text("**تـم تـفـعـيـل وضـع الـصـيـانـة.**\n\nلـن يـسـتـطـيـع الـأعـضـاء اسـتـخـدام الـبـوت حـتـى تـقـوم بـتـعـطـيـلـه.")
                
        elif state in ["disable", "تعطيل", "إيقاف", "off"]:
            if not await safe_db_call(is_maintenance):
                await message.reply_text("وضـع الـصـيـانـة مـعـطّـل بـالـفـعـل!")
            else:
                await safe_db_call(maintenance_off)
                await message.reply_text("**تـم تـعـطـيـل وضـع الـصـيـانـة.**\n\nيـمـكـن لـلـجـمـيـع اسـتـخـدام الـبـوت الـآن.")
                
        else:
            await message.reply_text("أمـر غـيـر صـحـيـح.")
    except Exception as e:
         await message.reply_text(f"**حـدث خـطـأ:** {e}")


# 3. أوامر السجل (Logger) (للمطور فقط)
@app.on_message(filters.command(["logger", "السجل"], prefixes=["/", "!", ".", ""]) & filters.user(OWNER_ID))
async def logger_toggle(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**طـريـقـة اسـتـخـدام إشـعـارات الـسـجـل:**\n\n"
            "• لـتـفـعـيـل الـسـجـل ارسـل: الـسـجـل تـفـعـيـل\n"
            "• لـتـعـطـيـل الـسـجـل ارسـل: الـسـجـل تـعـطـيـل"
        )

    state = message.text.split(None, 1)[1].strip().lower()
    
    try:
        if state in ["enable", "تفعيل", "on"]:
            if await safe_db_call(is_on_off, 2):
                await message.reply_text("إشـعـارات الـسـجـل مـفـعّـلـة بـالـفـعـل!")
            else:
                await safe_db_call(add_on, 2)
                await message.reply_text("**تـم تـفـعـيـل إشـعـارات الـسـجـل.**\n\nسـيـتـم إرسـال تـقـاريـر الـتـشـغـيـل إلـى جـروب الـسـجـل.")

        elif state in ["disable", "تعطيل", "off"]:
            if not await safe_db_call(is_on_off, 2):
                await message.reply_text("إشـعـارات الـسـجـل مـعـطّـلـة بـالـفـعـل!")
            else:
                await safe_db_call(add_off, 2)
                await message.reply_text("**تـم تـعـطـيـل إشـعـارات الـسـجـل.**")
        else:
            await message.reply_text("أمـر غـيـر صـحـيـح.")
    except Exception as e:
        await message.reply_text(f"**حـدث خـطـأ:** {e}")


# 4. أمر سحب ملف السجل (Logs File)
@app.on_message(filters.command(["logs", "ملف السجل"], prefixes=["/", "!", ".", ""]) & filters.user(OWNER_ID))
async def get_log_file(client, message: Message):
    try:
        if os.path.exists("log.txt"):
            await message.reply_document(
                document="log.txt",
                caption="**تـم سـحـب مـلـف الـسـجـلـات (Logs) بـنـجـاح.**"
            )
        else:
            await message.reply_text("**لا يـوجـد مـلـف سـجـلـات حـالـيـاً.**")
    except Exception as e:
        await message.reply_text(f"**حـدث خـطـأ:** {e}")
