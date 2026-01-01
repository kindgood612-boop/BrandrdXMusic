import os
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import filters, Client, enums
from pyrogram.types import *
from logging import getLogger
from BrandrdXMusic import app
import config

LOGGER = getLogger(__name__)

# قائمة لتخزين المجموعات التي قامت بقفل الترحيب
disabled_welcome = []

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

# دالة قص الصورة بشكل دائري
def circle(pfp, size=(500, 500)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

# دالة دمج صورة البروفايل مع الخلفية والكتابة عليها
def welcomepic(pic, user, chatname, id, uname):
    background = Image.open("BrandrdXMusic/assets/Brandedwel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((825, 824)) # حجم صورة البروفايل
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('BrandrdXMusic/assets/font.ttf', size=110)
    
    # كتابة الآيدي
    draw.text((2100, 1420), f'ID: {id}', fill=(255, 255, 255), font=font)
    
    # مكان وضع صورة البروفايل
    pfp_position = (1990, 435)
    background.paste(pfp, pfp_position, pfp)
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

# ---------------------------------------------------------------------------------
# أوامر القفل والفتح
# ---------------------------------------------------------------------------------

@app.on_message(filters.command(["قفل الترحيب", "تعطيل الترحيب"], prefixes=["/", "!", ".", ""]) & filters.group)
async def disable_welcome_cmd(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, user_id)
    
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        if chat_id not in disabled_welcome:
            disabled_welcome.append(chat_id)
            await message.reply("• تـم قـفـل الـتـرحـيـب بـنـجـاح")
        else:
            await message.reply("• الـتـرحـيـب مـقـفـل بـالـفـعـل")
    else:
        await message.reply("• هـذا الامـر لـلـمـشـرفـيـن فـقـط")

@app.on_message(filters.command(["فتح الترحيب", "تفعيل الترحيب"], prefixes=["/", "!", ".", ""]) & filters.group)
async def enable_welcome_cmd(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, user_id)
    
    if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        if chat_id in disabled_welcome:
            disabled_welcome.remove(chat_id)
            await message.reply("• تـم فـتـح الـتـرحـيـب بـنـجـاح")
        else:
            await message.reply("• الـتـرحـيـب مـفـتـوح بـالـفـعـل")
    else:
        await message.reply("• هـذا الامـر لـلـمـشـرفـيـن فـقـط")

# ---------------------------------------------------------------------------------

# الأمر اليدوي لتجربة الترحيب
@app.on_message(filters.command(["ترحيب", "welcome"], prefixes=["/", "!", ".", ""]))
async def test_welcome(client, message):
    user = message.from_user
    chat = message.chat
    
    # محاولة جلب صورة المستخدم
    try:
        if user.photo:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        else:
            # صورة افتراضية اذا لم يضع صورة
            pic = "BrandrdXMusic/assets/Brandedwel2.png" 
    except Exception:
        pic = "BrandrdXMusic/assets/Brandedwel2.png"
    
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, chat.title, user.id, user.username
        )
        await app.send_photo(
            chat.id,
            photo=welcomeimg,
            caption=f"""
• نــورت الـمـجـمـوعـة يـا » {user.first_name}
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
• الاســـم » {user.mention}
• الايـدي » `{user.id}`
• الـيـوزر » @{user.username}
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
""",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"• اضـف الـبـوت لـمـجـمـوعـتـك •", url=f"https://t.me/{app.username}?startgroup=true")]])
        )
    except Exception as e:
        LOGGER.error(e)
        await message.reply(f"حدث خطأ: {e}")
    
    # حذف الصور المؤقتة لتوفير المساحة
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        if user.photo:
            os.remove(f"downloads/pp{user.id}.png")
    except Exception:
        pass

# الترحيب التلقائي عند الانضمام
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    
    # التحقق مما إذا كان الترحيب مقفلاً في هذه المجموعة
    if chat_id in disabled_welcome:
        return

    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    
    # تحديد المستخدم الجديد
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    
    # محاولة جلب صورة المستخدم
    try:
        if user.photo:
            pic = await app.download_media(
                user.photo.big_file_id, file_name=f"pp{user.id}.png"
            )
        else:
            pic = "BrandrdXMusic/assets/Brandedwel2.png"
    except Exception:
        pic = "BrandrdXMusic/assets/Brandedwel2.png"
        
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
            
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"""
• نــورت الـمـجـمـوعـة يـا » {user.first_name}
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
• الاســـم » {user.mention}
• الايـدي » `{user.id}`
• الـيـوزر » @{user.username}
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
""",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"• اضـف الـبـوت لـمـجـمـوعـتـك •", url=f"https://t.me/{app.username}?startgroup=true")]])
        )
    except Exception as e:
        LOGGER.error(e)
        
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        if user.photo:
            os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        pass

# إشعار دخول البوت لمجموعة جديدة
@app.on_message(filters.new_chat_members & filters.group, group=-1)
async def bot_wel(_, message):
    for u in message.new_chat_members:
        if u.id == app.me.id:
            try:
                await app.send_message(config.LOG_GROUP_ID, f"""
• تـم تـفـعـيـل الـبـوت فـي مـجـمـوعـة جـديـدة
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
• الاســـم » {message.chat.title}
• الايـدي » {message.chat.id}
• الـيـوزر » @{message.chat.username}
ـــــــــــــــــــــــــــــــــــــــــــــــــــــــ
""")
            except:
                pass

__HELP__ = """
**اوامر الترحيب**

- ترحيب : لعرض بطاقة الترحيب الخاصة بك (تجربة).
- قفل الترحيب : لتعطيل الترحيب في المجموعة (مشرفين فقط).
- فتح الترحيب : لتفعيل الترحيب في المجموعة (مشرفين فقط).
"""

__MODULE__ = "الترحيب"
