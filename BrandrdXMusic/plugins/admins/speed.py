from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from BrandrdXMusic import app
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.misc import SUDOERS, db
from BrandrdXMusic.utils.decorators import AdminRightsCheck
from BrandrdXMusic.core.database import is_active_chat, is_nonadmin_chat
from BrandrdXMusic.utils.decorators.language import languageCB
from BrandrdXMusic.utils.inline import close_markup, speed_markup
from config import BANNED_USERS, adminlist

checker = []


# =======================
# أمر السرعة
# =======================
@app.on_message(
    filters.command(
        [
            "cspeed", "speed", "cslow", "slow", "playback", "cplayback",
            "سرعة", "سرعه", "بطئ", "قسرعة", "قبطئ"
        ],
        prefixes=["/", "@", ".", "#", ""]
    )
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def playback(client, message: Message, _, chat_id):
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])

    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["admin_27"])

    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await message.reply_text(_["admin_27"])

    buttons = speed_markup(_, chat_id)
    return await message.reply_text(
        text=_["admin_28"].format(app.mention),
        reply_markup=buttons,
    )


# =======================
# Callback تغيير السرعة
# =======================
@app.on_callback_query(filters.regex("^SpeedUP") & ~BANNED_USERS)
@languageCB
async def speedup_callback(client, query: CallbackQuery, _):
    data = query.data.split(None, 1)[1]
    chat, speed = data.split("|")
    chat_id = int(chat)

    if not await is_active_chat(chat_id):
        return await query.answer(_["general_5"], show_alert=True)

    # تحقق من الصلاحيات
    if not await is_nonadmin_chat(query.message.chat.id):
        if query.from_user.id not in SUDOERS:
            admins = adminlist.get(query.message.chat.id)
            if not admins or query.from_user.id not in admins:
                return await query.answer(_["admin_14"], show_alert=True)

    playing = db.get(chat_id)
    if not playing:
        return await query.answer(_["queue_2"], show_alert=True)

    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await query.answer(_["admin_27"], show_alert=True)

    file_path = playing[0]["file"]
    if "downloads" not in file_path:
        return await query.answer(_["admin_27"], show_alert=True)

    current_speed = playing[0].get("speed", "1.0")
    if str(current_speed) == str(speed):
        return await query.answer(_["admin_29"], show_alert=True)

    if chat_id in checker:
        return await query.answer(_["admin_30"], show_alert=True)

    checker.append(chat_id)

    await query.answer(_["admin_31"])
    msg = await query.edit_message_text(
        _["admin_32"].format(query.from_user.mention)
    )

    try:
        await Hotty.speedup_stream(
            chat_id,
            file_path,
            speed,
            playing,
        )
    except:
        checker.remove(chat_id)
        return await msg.edit_text(_["admin_33"], reply_markup=close_markup(_))

    checker.remove(chat_id)
    await msg.edit_text(
        _["admin_34"].format(speed, query.from_user.mention),
        reply_markup=close_markup(_),
    )
