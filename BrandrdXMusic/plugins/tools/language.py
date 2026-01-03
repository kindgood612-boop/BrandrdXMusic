from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)

from BrandrdXMusic import app
from BrandrdXMusic.core.database import get_lang, set_lang
from BrandrdXMusic.utils.decorators import ActualAdminCB, language, languageCB
from config import BANNED_USERS
from strings import get_string, languages_present


def lanuages_keyboard(_):
    buttons = []

    row = []
    for i in languages_present:
        row.append(
            InlineKeyboardButton(
                text=languages_present[i],
                callback_data=f"languages:{i}",
            )
        )
        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settingsback_helper",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ]
    )

    return InlineKeyboardMarkup(buttons)


@app.on_message(
    filters.command(["lang", "setlang", "language", "لغة", "تغيير اللغة"])
    & ~BANNED_USERS
)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["lang_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, callback_query: CallbackQuery, _):
    langauge = callback_query.data.split(":")[1]
    old = await get_lang(callback_query.message.chat.id)

    if str(old) == str(langauge):
        return await callback_query.answer(_["lang_4"], show_alert=True)

    try:
        _ = get_string(langauge)
        await callback_query.answer(_["lang_2"], show_alert=True)
    except:
        _ = get_string(old)
        return await callback_query.answer(
            _["lang_3"],
            show_alert=True,
        )

    await set_lang(callback_query.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    await callback_query.edit_message_reply_markup(reply_markup=keyboard)
