import os
import re
import asyncio
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
)

# ------------------------------------------------------------------
# استيراد المتغيرات والإعدادات الخاصة بالبوت
# ------------------------------------------------------------------
from config import (
    BANNED_USERS,                  # قائمة المستخدمين المحظورين
    SONG_DOWNLOAD_DURATION,         # الحد الافتراضي لمدة الأغنية بالدقائق
    SONG_DOWNLOAD_DURATION_LIMIT,   # الحد الأقصى للتحميل بالثواني
)

from BrandrdXMusic import YouTube, app
from BrandrdXMusic.utils.decorators.language import language, languageCB
from BrandrdXMusic.utils.formatters import convert_bytes
from BrandrdXMusic.utils.inline.song import song_markup

# ------------------------------------------------------------------
# دالة تحميل داخلية (بديلة عن الدوال الخارجية المعطلة)
# ------------------------------------------------------------------
def download_internal(url, stype, format_id):
    """
    تقوم هذه الدالة بتنزيل الفيديو أو الصوت باستخدام yt_dlp
    :param url: رابط الفيديو على يوتيوب
    :param stype: نوع التنزيل "video" أو "audio"
    :param format_id: معرّف الصيغة المطلوبة
    :return: مسار الملف النهائي بعد التنزيل
    """
    opts = {
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
        "cookiefile": "cookies.txt" if os.path.exists("cookies.txt") else None
    }

    if stype == "video":
        opts["format"] = f"{format_id}+bestaudio/best"
        opts["merge_output_format"] = "mp4"
    else:  # audio
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    try:
        with yt_dlp.YoutubeDL(opts) as ytdl:
            info = ytdl.extract_info(url, download=True)
            filename = ytdl.prepare_filename(info)
            if stype == "audio":
                base, _ = os.path.splitext(filename)
                return f"{base}.mp3"
            elif stype == "video":
                base, _ = os.path.splitext(filename)
                return f"{base}.mp4"
            return filename
    except Exception as e:
        print(f"Download Error: {e}")
        raise e

# ------------------------------------------------------------------
# أمر الأغاني الرئيسي
# ------------------------------------------------------------------
@app.on_message(filters.command(["song", "يوت"], prefixes=["", "/"]) & ~BANNED_USERS)
@language
async def song_command(client: Client, message: Message, _):
    """
    أمر تحميل الأغاني سواء رابط أو اسم الأغنية
    """
    # حذف الرسالة لو كانت تحتوي على "/"
    if message.text.startswith("/"):
        await message.delete()

    # محاولة استخراج الرابط من الرسالة
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(url)

        if duration_min is None:
            return await mystic.edit_text(_["song_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(_["play_4"].format(
                SONG_DOWNLOAD_DURATION, duration_min
            ))

        buttons = song_markup(_, vidid)
        await mystic.delete()
        await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    # لو الأمر بدون رابط، البحث بالكلمة
    if len(message.command) < 2:
        return await message.reply_text(_["song_2"])

    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        title, duration_min, duration_sec, thumbnail, vidid = await YouTube.details(query)
    except Exception:
        return await mystic.edit_text(_["play_3"])

    if duration_min is None:
        return await mystic.edit_text(_["song_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(_["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min))

    buttons = song_markup(_, vidid)
    await mystic.delete()
    await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ------------------------------------------------------------------
# Callback: العودة للخلف
# ------------------------------------------------------------------
@app.on_callback_query(filters.regex(r"song_back") & ~BANNED_USERS)
@languageCB
async def songs_back_helper(client, callback_query: CallbackQuery, _):
    """
    عند الضغط على زر العودة، إعادة عرض قائمة الصيغ
    """
    _, callback_request = callback_query.data.split(None, 1)
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    await callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))

# ------------------------------------------------------------------
# Callback: اختيار صيغة الأغنية
# ------------------------------------------------------------------
@app.on_callback_query(filters.regex(r"song_helper") & ~BANNED_USERS)
@languageCB
async def song_helper_cb(client, callback_query: CallbackQuery, _):
    """
    عند الضغط على زر الخيارات، عرض جميع صيغ الصوت أو الفيديو المتاحة
    """
    _, callback_request = callback_query.data.split(None, 1)
    stype, vidid = callback_request.split("|")

    try:
        await callback_query.answer(_["song_6"], show_alert=True)
    except:
        pass

    try:
        formats_available, _ = await YouTube.formats(vidid, True)
    except Exception:
        return await callback_query.edit_message_text(_["song_7"])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    done = []

    for x in formats_available:
        check = x["format"]
        if stype == "audio" and "audio" in check:
            if x["filesize"] is None:
                continue
            form = x["format_note"].title()
            if form in done:
                continue
            done.append(form)
            sz = convert_bytes(x["filesize"])
            fom = x["format_id"]
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=f"{form} Quality Audio = {sz}", callback_data=f"song_download {stype}|{fom}|{vidid}")]
            )
        elif stype == "video":
            if x["filesize"] is None:
                continue
            if int(x["format_id"]) not in [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]:
                continue
            sz = convert_bytes(x["filesize"])
            ap = check.split("-")[1]
            keyboard.inline_keyboard.append(
                [InlineKeyboardButton(text=f"{ap} = {sz}", callback_data=f"song_download {stype}|{x['format_id']}|{vidid}")]
            )

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data=f"song_back {stype}|{vidid}"),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
    ])

    await callback_query.edit_message_reply_markup(reply_markup=keyboard)

# ------------------------------------------------------------------
# Callback: تنزيل الأغنية أو الفيديو
# ------------------------------------------------------------------
@app.on_callback_query(filters.regex(r"song_download") & ~BANNED_USERS)
@languageCB
async def song_download_cb(client, callback_query: CallbackQuery, _):
    """
    تحميل الأغنية أو الفيديو بعد اختيار الصيغة من المستخدم
    """
    try:
        await callback_query.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    except:
        pass

    _, callback_request = callback_query.data.split(None, 1)
    stype, format_id, vidid = callback_request.split("|")
    mystic = await callback_query.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    # جلب معلومات الفيديو دون تحميل
    try:
        with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
            x = ytdl.extract_info(yturl, download=False)
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(e))

    title = re.sub("\W+", " ", x["title"].title())
    try:
        thumb_image_path = await callback_query.message.download()
    except:
        thumb_image_path = None
    duration = x["duration"]

    # تنزيل الملف باستخدام الدالة الداخلية
    loop = asyncio.get_event_loop()
    try:
        file_path = await loop.run_in_executor(None, download_internal, yturl, stype, format_id)
    except Exception as e:
        return await mystic.edit_text(_["song_9"].format(e))

    # إرسال الفيديو أو الصوت
    if stype == "video":
        width, height = (callback_query.message.photo.width, callback_query.message.photo.height) if thumb_image_path else (1280, 720)
        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(callback_query.message.chat.id, "upload_video")
    else:
        med = InputMediaAudio(
            media=file_path,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=x.get("uploader", "Unknown")
        )
        await mystic.edit_text(_["song_11"])
        await app.send_chat_action(callback_query.message.chat.id, "upload_audio")

    try:
        await callback_query.edit_message_media(media=med)
    except Exception as e:
        print(e)
        return await mystic.edit_text(_["song_10"])

    # حذف الملفات المؤقتة بعد الإرسال
    os.remove(file_path)
    if thumb_image_path:
        os.remove(thumb_image_path)
