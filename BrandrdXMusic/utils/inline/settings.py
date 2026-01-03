from typing import Union
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# =======================
# Main Settings Menu
# =======================

def setting_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU"),
                InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG"),
            ],
            [
                InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM"),
            ],
            [
                InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM"),
            ],
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Vote Mode Settings
# =======================

def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Vᴏᴛɪɴɢ ᴍᴏᴅᴇ ➜",
                    callback_data="VOTEANSWER",
                ),
                InlineKeyboardButton(
                    text=_["ST_B_5"] if mode else _["ST_B_6"],
                    callback_data="VOMODECHANGE",
                ),
            ],
            [
                InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M"),
                InlineKeyboardButton(
                    text=f"ᴄᴜʀʀᴇɴᴛ : {current}",
                    callback_data="ANSWERVOMODE",
                ),
                InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A"),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_helper",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Authorized Users Settings
# =======================

def auth_users_markup(_, status: Union[bool, str] = None):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["ST_B_7"],
                    callback_data="AUTHANSWER",
                ),
                InlineKeyboardButton(
                    text=_["ST_B_8"] if status else _["ST_B_9"],
                    callback_data="AUTH",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_1"],
                    callback_data="AUTHLIST",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_helper",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Play Mode Settings
# =======================

def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["ST_B_10"],
                    callback_data="SEARCHANSWER",
                ),
                InlineKeyboardButton(
                    text=_["ST_B_11"] if Direct else _["ST_B_12"],
                    callback_data="MODECHANGE",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_13"],
                    callback_data="AUTHANSWER",
                ),
                InlineKeyboardButton(
                    text=_["ST_B_8"] if Group else _["ST_B_9"],
                    callback_data="CHANNELMODECHANGE",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_14"],
                    callback_data="PLAYTYPEANSWER",
                ),
                InlineKeyboardButton(
                    text=_["ST_B_8"] if Playtype else _["ST_B_9"],
                    callback_data="PLAYTYPECHANGE",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_helper",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Audio Quality Settings
# =======================

def audio_quality_markup(
    _,
    low: Union[bool, str] = None,
    medium: Union[bool, str] = None,
    high: Union[bool, str] = None,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["ST_B_8"].format("✅" if low else ""),
                    callback_data="LQA",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_9"].format("✅" if medium else ""),
                    callback_data="MQA",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_10"].format("✅" if high else ""),
                    callback_data="HQA",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settingsback_helper",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Video Quality Settings
# =======================

def video_quality_markup(
    _,
    low: Union[bool, str] = None,
    medium: Union[bool, str] = None,
    high: Union[bool, str] = None,
):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["ST_B_11"].format("✅" if low else ""),
                    callback_data="LQV",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_12"].format("✅" if medium else ""),
                    callback_data="MQV",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["ST_B_13"].format("✅" if high else ""),
                    callback_data="HQV",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settingsback_helper",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
