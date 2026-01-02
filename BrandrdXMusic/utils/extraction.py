from pyrogram.enums import MessageEntityType
from pyrogram.types import Message, User
from BrandrdXMusic import app

async def extract_user(m: Message) -> User:
    # الـتـحـقـق مـن الـرد عـلـى رِسـالـة أولاً
    if m.reply_to_message:
        return m.reply_to_message.from_user

    # الـتـأكـد مـن وجـود مـعـطـيـات بـعـد الأمـر لـتـجـنـب الأخـطـاء
    if not m.command or len(m.command) < 2:
        return None

    # الـبـحـث عـن الـمـنـشـن الـنـصـي (الأسـمـاء الـزرقـاء بـدون يـوزر)
    if m.entities:
        for entity in m.entities:
            if entity.type == MessageEntityType.TEXT_MENTION:
                return entity.user

    # مـحـاولـة جـلـب الـمـسـتـخـدم عـن طـريـق الـيـوزر أو الآيـدي
    try:
        return await app.get_users(m.command[1])
    except Exception:
        return None
