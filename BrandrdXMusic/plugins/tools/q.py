import asyncio
from io import BytesIO
from httpx import AsyncClient, Timeout
from pyrogram import filters
from pyrogram.types import Message
from BrandrdXMusic import app

# --------------------------------------------------------------------------------- #

# إعدادات العميل
fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "ar-SA",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)

# لون الخلفية
THEME_COLOR = "#1b1429"

class QuotlyException(Exception):
    pass

# --------------------------------------------------------------------------------- #
# دوال استخراج البيانات

async def get_message_sender_id(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name: return 1
        if ctx.forward_from: return ctx.forward_from.id
        if ctx.forward_from_chat: return ctx.forward_from_chat.id
        return 1
    if ctx.from_user: return ctx.from_user.id
    if ctx.sender_chat: return ctx.sender_chat.id
    return 1

async def get_message_sender_name(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name: return ctx.forward_sender_name
        if ctx.forward_from:
            return f"{ctx.forward_from.first_name} {ctx.forward_from.last_name or ''}".strip()
        if ctx.forward_from_chat: return ctx.forward_from_chat.title
        return ""
    if ctx.from_user:
        return f"{ctx.from_user.first_name} {ctx.from_user.last_name or ''}".strip()
    if ctx.sender_chat: return ctx.sender_chat.title
    return ""

async def get_message_sender_username(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_from and ctx.forward_from.username: return ctx.forward_from.username
        if ctx.forward_from_chat and ctx.forward_from_chat.username: return ctx.forward_from_chat.username
        return ""
    if ctx.from_user and ctx.from_user.username: return ctx.from_user.username
    if ctx.sender_chat and ctx.sender_chat.username: return ctx.sender_chat.username
    return ""

async def get_message_sender_photo(ctx: Message):
    def extract_photo(obj):
        if obj and obj.photo:
            return {
                "small_file_id": obj.photo.small_file_id,
                "small_photo_unique_id": obj.photo.small_photo_unique_id,
                "big_file_id": obj.photo.big_file_id,
                "big_photo_unique_id": obj.photo.big_photo_unique_id,
            }
        return ""

    if ctx.forward_date:
        if ctx.forward_from: return extract_photo(ctx.forward_from)
        if ctx.forward_from_chat: return extract_photo(ctx.forward_from_chat)
        return ""
    if ctx.from_user: return extract_photo(ctx.from_user)
    if ctx.sender_chat: return extract_photo(ctx.sender_chat)
    return ""

async def get_text_or_caption(ctx: Message):
    return ctx.text or ctx.caption or ""

# --------------------------------------------------------------------------------- #
# الدالة الرئيسية (تم تحديث الرابط هنا)

async def pyrogram_to_quotly(messages, is_reply):
    if not isinstance(messages, list):
        messages = [messages]
    
    payload = {
        "type": "quote",
        "format": "png",
        "backgroundColor": THEME_COLOR,
        "messages": [],
    }

    for message in messages:
        msg_data = {
            "entities": [{"type": e.type.name.lower(), "offset": e.offset, "length": e.length} 
                         for e in (message.entities or message.caption_entities or [])],
            "chatId": await get_message_sender_id(message),
            "text": await get_text_or_caption(message),
            "avatar": True,
            "from": {
                "id": await get_message_sender_id(message),
                "name": await get_message_sender_name(message),
                "username": await get_message_sender_username(message),
                "type": message.chat.type.name.lower(),
                "photo": await get_message_sender_photo(message)
            }
        }

        if message.reply_to_message and is_reply:
            msg_data["replyMessage"] = {
                "name": await get_message_sender_name(message.reply_to_message),
                "text": await get_text_or_caption(message.reply_to_message),
                "chatId": await get_message_sender_id(message.reply_to_message),
            }
        else:
            msg_data["replyMessage"] = {}
            
        payload["messages"].append(msg_data)

    # هنا تم وضع الرابط الجديد الخاص بك
    response = await fetch.post("https://quote-api-amber-beta.vercel.app/generate", json=payload)
    
    if not response.is_error:
        return response.read()
    raise QuotlyException(response.json())

def isArgInt(txt) -> list:
    try:
        return [True, int(txt)]
    except ValueError:
        return [False, 0]

# --------------------------------------------------------------------------------- #
# معالج الأوامر

@app.on_message(filters.command(["اقتباس", "صوري", "q", "r"], prefixes=["/", "!", "."]) & filters.reply)
async def msg_quotly_cmd(client, message: Message):
    
    try:
        await message.delete()
    except:
        pass

    wait_msg = await message.reply_text("**جـاري صـنـع الـمـلـصـق...** 🤍")
    
    is_reply = False
    if message.command[0] in ["صوري", "r"]:
        is_reply = True

    if len(message.command) > 1:
        check_arg = isArgInt(message.command[1])
        if check_arg[0]:
            count = check_arg[1]
            if count < 2 or count > 10:
                await wait_msg.delete()
                return await message.reply_text("**الـعـدد الـمـسـمـوح بـيـن 2 و 10 فـقـط** 🧚")
            
            try:
                messages = [
                    i for i in await client.get_messages(
                        chat_id=message.chat.id,
                        message_ids=range(
                            message.reply_to_message.id,
                            message.reply_to_message.id + count
                        ),
                        replies=-1,
                    )
                    if not i.empty and not i.media
                ]
            except Exception:
                await wait_msg.delete()
                return await message.reply_text("**حـدث خـطـأ فـي جـلـب الـرسـائـل**")

            try:
                make_quotly = await pyrogram_to_quotly(messages, is_reply=is_reply)
                bio_sticker = BytesIO(make_quotly)
                bio_sticker.name = "sticker.webp"
                
                await wait_msg.delete()
                return await message.reply_sticker(bio_sticker)
            except Exception:
                await wait_msg.delete()
                return await message.reply_text("**حـدث خـطـأ أثـنـاء الـتـصـمـيـم**")

    try:
        messages = [message.reply_to_message]
        make_quotly = await pyrogram_to_quotly(messages, is_reply=is_reply)
        
        bio_sticker = BytesIO(make_quotly)
        bio_sticker.name = "sticker.webp"
        
        await wait_msg.delete()
        return await message.reply_sticker(bio_sticker)
        
    except Exception as e:
        await wait_msg.delete()
        # await message.reply_text(f"Error: {e}")
        pass
