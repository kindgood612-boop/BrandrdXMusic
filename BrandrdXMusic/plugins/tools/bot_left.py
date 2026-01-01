import random
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)
from config import LOGGER_ID as LOG_GROUP_ID
from BrandrdXMusic import app
from BrandrdXMusic.utils.database import get_assistant
from BrandrdXMusic.utils.database import delete_served_chat

# الروابط الجديدة للصور
photo = [
    "https://files.catbox.moe/wqipfn.jpg",
    "https://files.catbox.moe/4qhfqw.jpg",
    "https://files.catbox.moe/b6533n.jpg",
    "https://files.catbox.moe/b91yyd.jpg",
    "https://files.catbox.moe/xi3mb1.jpg",
]


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == (await app.get_me()).id:
            remove_by = (
                message.from_user.mention if message.from_user else "مـسـتـخـدم مـجـهـول"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "مـجـمـوعـة خـاصـة"
            )
            chat_id = message.chat.id
            left = (
                f"✫ **خـروج مـن مـجـمـوعـة** 🥀\n\n"
                f"**اسـم الـمـجـمـوعـة :** {title}\n\n"
                f"**آيـدي الـمـجـمـوعـة :** `{chat_id}`\n\n"
                f"**تـم طـردي بـواسـطـة :** {remove_by}\n\n"
                f"**الـبـوت :** @{app.username} 🤍"
            )
            await app.send_photo(LOG_GROUP_ID, photo=random.choice(photo), caption=left)
            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        return
