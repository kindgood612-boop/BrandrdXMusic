import os
import shutil
from re import findall
from bing_image_downloader import downloader
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, Message
from BrandrdXMusic import app

# --- أوامر البحث عن صور ---
COMMANDS = ["img", "image", "صور", "صورة"]

@app.on_message(filters.command(COMMANDS))
async def google_img_search(client: Client, message: Message):
    chat_id = message.chat.id

    # 1. التحقق من وجود كلمة بحث
    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply_text("**يـرجـى كـتـابـة اسـم الـصـورة بـعـد الأمـر.**")

    # 2. استخراج العدد المطلوب (اختياري)
    # مثال: /صور قطط lim=7
    lim = findall(r"lim=\d+", query)
    try:
        if lim:
            limit_count = int(lim[0].replace("lim=", ""))
            query = query.replace(lim[0], "").strip()
        else:
            limit_count = 5 # العدد الافتراضي
            
        # وضع حد أقصى للصور (مثلاً 10) لتجنب تعليق البوت
        if limit_count > 10:
            limit_count = 10
            
    except Exception:
        limit_count = 5

    # رسالة الانتظار
    status_msg = await message.reply_text("**جـاري الـبـحـث عـن الـصـور...**")
    
    download_dir = "downloads"
    
    # اسم المجلد ليكون فريداً (لتجنب تداخل عمليات البحث)
    dir_name = f"{query}_{message.from_user.id}"
    full_path = os.path.join(download_dir, dir_name)

    try:
        # 3. بدء التحميل
        downloader.download(
            query, 
            limit=limit_count, 
            output_dir=download_dir, 
            adult_filter_off=True, 
            force_replace=False, 
            timeout=20, 
            verbose=False
        )
        
        # تصحيح المسار لأن المكتبة تنشئ مجلداً باسم البحث
        # ملاحظة: المكتبة تنشئ مجلداً داخل downloads باسم البحث query
        # لذا نبحث عن المجلد الصحيح
        target_dir = os.path.join(download_dir, query)
        
        if not os.path.exists(target_dir):
            await status_msg.edit("**لـم يـتـم الـعـثـور عـلى صـور.**")
            return

        images_list = [
            os.path.join(target_dir, img) 
            for img in os.listdir(target_dir) 
            if img.endswith(('.jpg', '.jpeg', '.png'))
        ][:limit_count]

        if not images_list:
            await status_msg.edit("**لـم يـتـم الـعـثـور عـلى صـور صـالـحـة.**")
            shutil.rmtree(target_dir, ignore_errors=True)
            return

        # 4. إرسال الصور كمجموعة
        await status_msg.edit("**جـاري رفـع الـصـور...**")
        
        await app.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=img) for img in images_list],
            reply_to_message_id=message.id
        )
        
        # حذف رسالة الانتظار
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit("**حـدث خـطـأ أثـنـاء الـبـحـث.**")
        print(f"Image Search Error: {e}")

    finally:
        # 5. تنظيف الملفات دائماً (سواء نجح أو فشل)
        # نحاول حذف مجلد البحث المحدد
        try:
            target_dir = os.path.join(download_dir, query)
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir, ignore_errors=True)
        except:
            pass
