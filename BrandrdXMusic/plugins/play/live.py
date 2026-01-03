import traceback
from pyrogram import filters
from BrandrdXMusic import YouTube, app
from BrandrdXMusic.utils.channelplay import get_channeplayCB
from BrandrdXMusic.utils.decorators.language import languageCB
from BrandrdXMusic.utils.stream.stream import stream
from config import BANNED_USERS


@app.on_callback_query(filters.regex("LiveStream") & ~BANNED_USERS)
@languageCB
async def play_live_stream(client, CallbackQuery, _):
    # استخراج البيانات من الزر
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")

    # التحقق من أن الشخص الذي ضغط الزر هو من طلب الأمر
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "هذا الأمر ليس لك",
                show_alert=True
            )
        except:
            return

    # التحقق من وضع تشغيل القنوات
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return

    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name

    # حذف الرسالة القديمة
    try:
        await CallbackQuery.message.delete()
    except:
        pass

    try:
        await CallbackQuery.answer("جاري المعالجة...", show_alert=False)
    except:
        pass

    # إرسال رسالة الانتظار
    mystic = await client.send_message(
        chat_id,
        f"جاري بدء البث المباشر عبر القناة\n\nالقناة: {channel}"
        if channel
        else "جاري بدء تشغيل البث المباشر"
    )

    # جلب معلومات الفيديو من يوتيوب
    try:
        details, _ = await YouTube.track(vidid, True)
    except:
        return await mystic.edit_text(
            "فشل في جلب معلومات الفيديو، حاول مرة أخرى لاحقاً."
        )

    ffplay = True if fplay == "f" else None

    # التحقق الصحيح من أن الرابط بث مباشر
    duration = details.get("duration_min")

    if not duration or duration in ["0:00", "LIVE"]:
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
                spotify=False,
            )
        except Exception as e:
            traceback.print_exc()
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else f"حدث خطأ غير متوقع: {ex_type}"
            return await mystic.edit_text(
                f"حدث خطأ أثناء التشغيل\n{err}"
            )
    else:
        return await mystic.edit_text(
            "هذا الرابط ليس بثاً مباشراً (Live Stream)"
        )

    # تنظيف رسالة الانتظار بعد النجاح
    try:
        await mystic.delete()
    except:
        pass
