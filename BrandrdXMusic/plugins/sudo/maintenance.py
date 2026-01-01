from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from config import OWNER_ID
from BrandrdXMusic.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from strings import get_string


# 1. الحارس (يعمل أولاً): يتحقق من الصيانة ويرد على العضو من ملف الترجمة
@app.on_message(filters.all & ~filters.user(OWNER_ID), group=-1)
async def maintenance_check(client, message: Message):
    if await is_maintenance():
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")
            
        # يقوم بالرد على العضو برسالة الصيانة (تأكد من وجود maint_6 في ملف strings)
        await message.reply_text(_["maint_6"])
        # يوقف البوت عن تنفيذ أي أمر آخر (مثل التشغيل)
        message.stop_propagation()


# 2. دالة التحكم (للمطور فقط)
@app.on_message(filters.command(["maintenance", "الصيانة"]) & filters.user(OWNER_ID))
async def maintenance(client, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except:
        _ = get_string("en")
        
    usage = _["maint_1"]
    
    if len(message.command) != 2:
        return await message.reply_text(usage)
        
    state = message.text.split(None, 1)[1].strip().lower()
    
    # أوامر التفعيل
    if state in ["enable", "تفعيل"]:
        if await is_maintenance():
            await message.reply_text(_["maint_4"])
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"].format(app.mention))
            
    # أوامر التعطيل
    elif state in ["disable", "تعطيل", "إيقاف", "ايقاف"]:
        if not await is_maintenance():
            await message.reply_text(_["maint_5"])
        else:
            await maintenance_off()
            await message.reply_text(_["maint_3"].format(app.mention))
            
    else:
        await message.reply_text(usage)
