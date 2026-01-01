import os
import asyncio
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from BrandrdXMusic import app

# --------------------------------------------------------------------------------- #

def get_font(font_size, font_path):
    return ImageFont.truetype(font_path, font_size)

# --------------------------------------------------------------------------------- #

async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: int,
    profile_path: str = None
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

# --------------------------------------------------------------------------------- #

bg_path = "BrandrdXMusic/assets/userinfo.png"
font_path = "BrandrdXMusic/assets/hiroko.ttf"

# --------------------------------------------------------------------------------- #

@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client, member: ChatMemberUpdated):
    
    if (
        member.new_chat_member 
        and member.new_chat_member.status not in [
            enums.ChatMemberStatus.BANNED, 
            enums.ChatMemberStatus.LEFT
        ]
    ):
        return

    user = member.old_chat_member.user if member.old_chat_member else member.from_user

    if user.photo and user.photo.big_file_id:
        try:
            photo = await app.download_media(user.photo.big_file_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )
        
            # تم حذف "نراك قريباً" وتعديل التنسيق
            caption = (
                f"**#غـادر_الـعـضـو** 🤍\n\n"
                f"**الاسـم :** {user.mention}\n"
                f"**لـقـد خـرج مـن الـمـجـمـوعـة** 🧚"
            )
            
            button_text = "• الـعـضـو •"

            deep_link = f"tg://openmessage?user_id={user.id}"

            message = await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)]
                ])
            )

            try:
                os.remove(photo)
                os.remove(welcome_photo)
            except:
                pass

            await asyncio.sleep(30)
            await message.delete()
            
        except Exception as e:
            print(f"Left Member Error: {e}")
            return
    else:
        pass
