from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from BrandrdXMusic import app
from BrandrdXMusic.core.call import Hotty
from BrandrdXMusic.utils import bot_sys_stats
from BrandrdXMusic.utils.decorators.language import language
from BrandrdXMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["بينج", "سرعة", "حياة", "ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    
    # رسالة الانتظار الأولى
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption="**جـاري قـيـاس سـرعـة الـبـوت...** 🤍",
    )
    
    # جلب الإحصائيات من السيرفر والمساعد
    pytgping = await Hotty.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    
    # تعديل الرسالة بالمعلومات النهائية
    await response.edit_text(
        f"""
**سـرعـة بـوت مـيـوزك** 🧚

**🧚 سـرعـة الاسـتـجـابـة :** {resp} مـلـي ثـانـيـة
**🤍 سـرعـة الـمـسـاعـد :** {pytgping}
**⚡ وقـت الـتـشـغـيـل :** {UP}
**🥀 الـرامـات :** {RAM}
**💞 الـمـعـالـج :** {CPU}
**♥️ الـمـسـاحـة :** {DISK}

**{app.mention}** 🤍
""",
        reply_markup=supp_markup(_),
    )
