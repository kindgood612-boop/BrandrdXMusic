from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.utils.database import set_cmode
from BrandrdXMusic.utils.decorators.admins import AdminActual
from config import BANNED_USERS


@app.on_message(filters.command(["channelplay", "ربط القناة", "تشغيل القناة", "ربط قناة"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>طريقة الاستخدام:</b>\n/channelplay [معرف القناة/مرتبطة/تعطيل]\n\n<b>مثال:</b>\n/channelplay @ChannelName"
        )
    
    query = message.text.split(None, 2)[1].lower().strip()
    
    # خيار التعطيل
    if (str(query)).lower() in ["disable", "تعطيل"]:
        await set_cmode(message.chat.id, None)
        return await message.reply_text("تم تعطيل وضع تشغيل القناة، سيتم التشغيل في المجموعة الآن.")
    
    # خيار القناة المرتبطة تلقائياً
    elif str(query) in ["linked", "مرتبطة"]:
        chat = await app.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                f"تم ربط التشغيل بالقناة المرتبطة: {chat.linked_chat.title}\nالمعرف: {chat.linked_chat.id}"
            )
        else:
            return await message.reply_text("هذه المجموعة لا تمتلك قناة مرتبطة بها في إعدادات تيليجرام.")
    
    # خيار ربط قناة محددة
    else:
        try:
            chat = await app.get_chat(query)
        except:
            return await message.reply_text("لم أستطع العثور على القناة، تأكد من المعرف أو أن البوت مشرف فيها.")
        
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text("هذا المعرف لا ينتمي لقناة.")
        
        try:
            async for user in app.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    cusn = user.user.username
                    crid = user.user.id
        except:
            return await message.reply_text("حدث خطأ، تأكد أنني مشرف في القناة أولاً.")
        
        if crid != message.from_user.id:
            return await message.reply_text(f"عذراً، يجب أن تكون مالك القناة لربطها.\nالمالك هو: @{cusn}")
        
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(f"تم ربط التشغيل بالقناة: {chat.title}\nالمعرف: {chat.id}")
