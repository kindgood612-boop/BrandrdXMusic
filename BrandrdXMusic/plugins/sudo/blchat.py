from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.misc import SUDOERS
from BrandrdXMusic.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from config import BANNED_USERS

# دالة حظر مجموعة من استخدام البوت
@app.on_message(filters.command(["blchat", "blacklistchat", "حظر_مجموعة", "حظر_شات"]) & SUDOERS)
async def blacklist_chat_func(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "🥀 **طـريـقـة الاسـتـخـدام :**\n\n"
            "• blchat [ايدي_المجموعة]\n"
            "• حظر_مجموعة [ايدي_المجموعة]"
        )
    
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text("🥀 **عـذراً، يـجـب أن يـكـون الآيـدي أرقـامـاً فـقـط.**")

    if chat_id in await blacklisted_chats():
        return await message.reply_text("🧚 **هـذه الـمـجـمـوعـة مـحـظـورة بـالـفـعـل.**")
    
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text(
            "♥️ **تـم حـظـر الـمـجـمـوعـة مـن اسـتـخـدام الـبـوت بـنـجـاح.**"
        )
        try:
            # محاولة مغادرة المجموعة بعد حظرها
            await app.leave_chat(chat_id)
        except:
            pass
    else:
        await message.reply_text("🥀 **حـدث خـطـأ أثـنـاء حـظـر الـمـجـمـوعـة.**")


# دالة رفع الحظر عن مجموعة
@app.on_message(filters.command(["whitelistchat", "unblacklistchat", "unblchat", "رفع_حظر", "رفع_الحظر"]) & SUDOERS)
async def white_funciton(client, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "🥀 **طـريـقـة الاسـتـخـدام :**\n\n"
            "• unblchat [ايدي_المجموعة]\n"
            "• رفع_حظر [ايدي_المجموعة]"
        )
    
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text("🥀 **عـذراً، يـجـب أن يـكـون الآيـدي أرقـامـاً فـقـط.**")

    if chat_id not in await blacklisted_chats():
        return await message.reply_text("🧚 **هـذه الـمـجـمـوعـة لـيـسـت مـحـظـورة أصـلاً.**")
    
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "💝 **تـم رفـع الـحـظـر عـن الـمـجـمـوعـة بـنـجـاح.**"
        )
    
    await message.reply_text("🥀 **حـدث خـطـأ أثـنـاء رفـع الـحـظـر.**")


# دالة عرض قائمة المجموعات المحظورة
@app.on_message(filters.command(["blchats", "blacklistedchats", "المجموعات_المحظورة"]) & ~BANNED_USERS)
async def all_chats(client, message: Message):
    text = "🥀 **قـائـمـة الـمـجـمـوعـات الـمـحـظـورة :**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except:
            title = "مـجـمـوعـة خـاصـة"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    
    if j == 0:
        await message.reply_text("💕 **لا تـوجـد مـجـمـوعـات مـحـظـورة حـالـيـاً.**")
    else:
        await message.reply_text(text)
