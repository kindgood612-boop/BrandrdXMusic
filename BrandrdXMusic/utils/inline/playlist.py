from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# =======================
# Playlist Main
# =======================

def botplaylist_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["PL_B_1"],
                    callback_data="get_playlist_playmode",
                ),
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
# Playlist Play Mode
# =======================

def get_playlist_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["P_B_1"],
                    callback_data="play_playlist audio",
                ),
                InlineKeyboardButton(
                    text=_["P_B_2"],
                    callback_data="play_playlist video",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="home_play",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Top Playlist
# =======================

def top_play_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["PL_B_9"],
                    callback_data="SERVERTOP global",
                )
            ],
            [
                InlineKeyboardButton(
                    text=_["PL_B_10"],
                    callback_data="SERVERTOP chat",
                )
            ],
            [
                InlineKeyboardButton(
                    text=_["PL_B_11"],
                    callback_data="SERVERTOP user",
                )
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="get_playmarkup",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


def failed_top_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="get_top_playlists",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )


# =======================
# Delete Playlist Warning
# =======================

def warning_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["PL_B_7"],
                    callback_data="delete_whole_playlist",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="del_back_playlist",
                ),
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )


# =======================
# Close Only
# =======================

def close_markup(_):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )
