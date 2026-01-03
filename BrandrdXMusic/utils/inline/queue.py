from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from BrandrdXMusic import app
from config import SUPPORT_CHAT

# =======================
# Static Links
# =======================

CHANNEL_LINK = "https://t.me/SourceBoda"
OWNER_LINK = "https://t.me/S_G0C7"


# =======================
# Queue Info Markup
# =======================

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[int, bool] = None,
    dur: Union[int, bool] = None,
):
    no_duration = [
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ]
    ]

    with_duration = [
        [
            InlineKeyboardButton(
                text=_["QU_B_2"].format(played, dur),
                callback_data="GetTimer",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["QU_B_1"],
                callback_data=f"GetQueued {CPLAY}|{videoid}",
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data="close",
            ),
        ],
    ]

    return InlineKeyboardMarkup(
        no_duration if DURATION == "Unknown" else with_duration
    )


# =======================
# Queue Back Button
# =======================

def queue_back_markup(_, CPLAY):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data=f"queue_back_timer {CPLAY}",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )


# =======================
# Admin Quick Actions (Running Stream)
# =======================

def aq_markup(_, chat_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}"),
                InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}"),
                InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
                InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
            ],
            [
                InlineKeyboardButton("「𝗼𝘄𝗻𝗲𝗿」", url=OWNER_LINK),
                InlineKeyboardButton("「قناة السورس」", url=CHANNEL_LINK),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                )
            ],
        ]
    )


# =======================
# Queue Controller Markup
# =======================

def queuemarkup(_, vidid, chat_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("▷", callback_data=f"ADMIN Resume|{chat_id}"),
                InlineKeyboardButton("II", callback_data=f"ADMIN Pause|{chat_id}"),
                InlineKeyboardButton("↻", callback_data=f"ADMIN Replay|{chat_id}"),
            ],
            [
                InlineKeyboardButton("‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
                InlineKeyboardButton("▢", callback_data=f"ADMIN Stop|{chat_id}"),
            ],
            [
                InlineKeyboardButton(
                    text=_["S_B_5"],
                    url=f"https://t.me/{app.username}?startgroup=true",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="قناة السورس",
                    url=CHANNEL_LINK,
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                )
            ],
        ]
    )
