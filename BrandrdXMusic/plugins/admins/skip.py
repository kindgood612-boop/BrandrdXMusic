from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup

import config
from BrandrdXMusic import app, YouTube
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import db
from BrandrdXMusic.core.database import get_loop
from BrandrdXMusic.utils.decorators import AdminRightsCheck
from BrandrdXMusic.utils.inline import close_markup, stream_markup, stream_markup2
from BrandrdXMusic.utils.stream.autoclear import auto_clean
from BrandrdXMusic.utils.thumbnails import get_thumb
from config import BANNED_USERS


@app.on_message(
    filters.command(
        ["skip", "cskip", "next", "cnext", "تخطي", "التالي", "سكب", "كسكب"],
        prefixes=["/", "@", ".", "#", ""]
    )
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def skip_track(client, message: Message, _, chat_id):
    requester = message.from_user.mention if message.from_user else message.chat.title

    # دعم القناة المرتبطة
    if message.command[0] in ["cskip", "cnext", "كسكب"]:
        if message.chat.linked_chat:
            chat_id = message.chat.linked_chat.id
            requester = message.chat.title

    # التحقق من اللوب
    if len(message.command) > 1:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(_["admin_8"])

        arg = message.command[1]
        if arg.isnumeric():
            skip_count = int(arg)
            queue = db.get(chat_id)

            if not queue:
                return await message.reply_text(_["queue_2"])

            if len(queue) <= 1:
                return await message.reply_text(_["admin_10"])

            max_skip = len(queue) - 1
            if skip_count > max_skip:
                return await message.reply_text(_["admin_11"].format(max_skip))

            for _ in range(skip_count):
                popped = queue.pop(0)
                await auto_clean(popped)

            if not queue:
                await message.reply_text(
                    _["admin_6"].format(requester, message.chat.title),
                    reply_markup=close_markup(_),
                )
                return await Hotty.stop_stream(chat_id)

    # تخطي افتراضي (أغنية واحدة)
    queue = db.get(chat_id)
    if not queue:
        return await message.reply_text(_["queue_2"])

    try:
        popped = queue.pop(0)
        await auto_clean(popped)
    except:
        await message.reply_text(
            _["admin_6"].format(requester, message.chat.title),
            reply_markup=close_markup(_),
        )
        return await Hotty.stop_stream(chat_id)

    if not queue:
        await message.reply_text(
            _["admin_6"].format(requester, message.chat.title),
            reply_markup=close_markup(_),
        )
        return await Hotty.stop_stream(chat_id)

    # تشغيل التالي
    track = queue[0]
    file_path = track["file"]
    title = track["title"].title()
    user = track["by"]
    streamtype = track["streamtype"]
    videoid = track["vidid"]
    is_video = streamtype == "video"

    db[chat_id][0]["played"] = 0

    if track.get("old_dur"):
        db[chat_id][0]["dur"] = track["old_dur"]
        db[chat_id][0]["seconds"] = track["old_second"]
        db[chat_id][0]["speed"] = 1.0
        db[chat_id][0]["speed_path"] = None

    try:
        if "live_" in file_path:
            _, link = await YouTube.video(videoid, True)
            image = await YouTube.thumbnail(videoid, True)
            await Hotty.skip_stream(chat_id, link, video=is_video, image=image)
            button = stream_markup2(_, chat_id)

        elif "vid_" in file_path:
            msg = await message.reply_text(_["call_7"])
            file_path, _ = await YouTube.download(videoid, msg, videoid=True, video=is_video)
            image = await YouTube.thumbnail(videoid, True)
            await Hotty.skip_stream(chat_id, file_path, video=is_video, image=image)
            await msg.delete()
            button = stream_markup(_, videoid, chat_id)

        elif "index_" in file_path:
            await Hotty.skip_stream(chat_id, videoid, video=is_video)
            button = stream_markup2(_, chat_id)

        else:
            image = await YouTube.thumbnail(videoid, True) if videoid not in ["telegram", "soundcloud"] else None
            await Hotty.skip_stream(chat_id, file_path, video=is_video, image=image)
            button = stream_markup(_, videoid, chat_id)

    except:
        return await message.reply_text(_["call_6"])

    img = (
        await get_thumb(videoid)
        if videoid not in ["telegram", "soundcloud"]
        else config.STREAM_IMG_URL
    )

    run = await message.reply_photo(
        photo=img,
        caption=_["stream_1"].format(
            f"https://t.me/{app.username}?start=info_{videoid}",
            title[:23],
            track["dur"],
            user,
        ),
        reply_markup=InlineKeyboardMarkup(button),
    )

    db[chat_id][0]["mystic"] = run
    db[chat_id][0]["markup"] = "stream"
