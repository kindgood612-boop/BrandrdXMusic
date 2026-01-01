import asyncio
import os
import re
import aiofiles
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton
from BrandrdXMusic import app
from BrandrdXMusic.utils.errors import capture_err
from BrandrdXMusic.utils.pastebin import HottyBin

# تحديد صيغ الملفات المسموح بها
pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")

# هذه الدالة تتحقق من عمل الرابط (لم يتم تغيير المنطق، فقط التعليقات)
async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with session.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.exceptions.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return True if status == 200 else False
    return False

# تم تغيير الأمر إلى (لصق - رابط - طباعة)
@app.on_message(filters.command(["لصق", "رابط", "طباعة"], prefixes=["/", "!", "."]))
@capture_err
async def paste_func(_, message):
    # التحقق من الرد على رسالة
    if not message.reply_to_message:
        return await message.reply_text("**قـم بـالـرد عـلـى نـص أو مـلـف لـرفـعـه..** 🤍")

    # رسالة انتظار
    m = await message.reply_text("**جـاري الـمـعـالـجـة والـرفـع...**")

    # معالجة النص المباشر
    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
        
    # معالجة الملفات
    elif message.reply_to_message.document:
        document = message.reply_to_message.document
        
        # التحقق من حجم الملف (1 ميجا)
        if document.file_size > 1048576:
            return await m.edit("**عـذراً، يـجـب أن يـكـون حـجـم الـمـلـف أقـل مـن 1 مـيـجـا.** 🧚")
            
        # التحقق من نوع الملف
        if not pattern.search(document.mime_type):
            return await m.edit("**عـذراً، يُـسـمـح فـقـط بـالـمـلـفـات الـنـصـيـة.** 🤍")
            
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc) # حذف الملف المؤقت

    # رفع النص إلى الموقع والحصول على الرابط
    link = await HottyBin(content)
    preview = link 
    
    # إعداد الزر
    button = InlineKeyboard(row_width=1)
    button.add(InlineKeyboardButton(text="• رابـط الـنـص •", url=link))

    # حذف رسالة الانتظار وإرسال النتيجة
    await m.delete()
    try:
        await message.reply(
            "**تـم اسـتـخـراج الـرابـط بـنـجـاح** 🧚",
            quote=False,
            reply_markup=button
        )
        
    except Exception:
        pass
