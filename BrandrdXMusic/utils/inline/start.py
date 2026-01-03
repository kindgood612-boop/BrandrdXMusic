from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from BrandrdXMusic import app


def start_panel(_):
    """
    Start panel shown in groups
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_1"],
                    url=f"https://t.me/{app.username}?startgroup=true",
                ),
                InlineKeyboardButton(
                    text=_["S_B_2"],
                    url=config.SUPPORT_CHAT,
                ),
            ],
        ]
    )


def private_panel(_):
    """
    Start panel shown in private chat
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["S_B_3"],
                    url=f"https://t.me/{app.username}?startgroup=true",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["S_B_4"],
                    callback_data="settings_back_helper",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["S_B_5"],
                    user_id=config.OWNER_ID,
                ),
                InlineKeyboardButton(
                    text=_["S_B_2"],
                    url=config.SUPPORT_CHAT,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["S_B_6"],
                    url=config.SUPPORT_CHANNEL,
                ),
            ],
        ]
    )
