from BrandrdXMusic import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

# قائمة الايموجي البسيطة
EMOJI = [ "🦋", "🌸", "🌹", "🍬", "⚡️", "✨", "🎈", "🧸", "🤍", "🌿", "🍉", "🍓", "☕️", "☁️", "💜", "🪴", "🐬", "🦄" ]

# قائمة الردود (نص عادي بدون زخرفة أو تغليظ)
TAGMES = [ 
    "منور يا غالي",
    "كيف حالك اليوم",
    "صلي على النبي",
    "وحشتني يا صاحبي",
    "منور الجروب كله",
    "ممكن نتعرف",
    "تعال نلعب شوي",
    "فينك مختفي",
    "يا بخت اللي عرفك",
    "اي العسل ده",
    "مرتبط ولا سنجل",
    "صباح الخير",
    "تصبح على خير يا قمر",
    "الجو جميل اليوم",
    "تكلم معنا",
    "تعشيت ولا لسه",
    "شاركنا بأغنية",
    "ليه ما بترسل رسائل",
    "انا بوت جميل",
    "كان يوم حلو امس",
    "كنت مشغول في ايه",
    "خليك هادي يا صديقي",
    "بتعرف تغني",
    "تعال نتمشى",
    "دايماً كون سعيد",
    "ممكن نكون اصدقاء",
    "متزوج ولا لسه",
    "بحبك في الله",
    "ضيف اصحابك هنا",
    "انبسط يا عم",
    "تعرف صاحب الجروب",
    "بتفكر فيني",
    "يلا نعمل حفلة",
    "كيف كان يومك",
    "اسمعني",
    "شفت اللي حصل",
    "انت ادمن هنا",
    "عندك كام سنة",
    "السجن للجدعان",
    "شفتك امبارح",
    "انت منين",
    "انت فاتح ولا قافل",
    "بتحب تاكل ايه",
    "ضفني في جروبك",
    "تلعب صراحة ولا جرأة",
    "ايه اللي حصل معك",
    "بتحب الشوكولاتة",
    "هلا يا حلو",
    "دردش معي",
    "بتقول ايه",
    "هات رقمك لو سمحت"
]

VC_TAG = [
    "استغفر الله",
    "انا ما بحبك",
    "اثبت نفسك",
    "انضم لقناتنا",
    "اسمك محفور بقلبي",
    "فين اصحابك",
    "تايه في حب مين",
    "بتشتغل ايه",
    "ساكن فين",
    "صباح العسل",
    "تصبح على خير",
    "انا زعلان النهاردة",
    "كلمني شوية",
    "هتاكل ايه النهاردة",
    "الدنيا ماشية ازاي",
    "ليه مش بترد",
    "انا بريء",
    "الجو كان حلو امس",
    "كنت مختفي فين",
    "انت مرتبط",
    "خليك رايق",
    "سمعنا صوتك",
    "تخرج معي",
    "افرح يا عم",
    "خلينا اصحاب",
    "خطبت ولا لسه",
    "كل دي غيبة",
    "الرابط في البايو",
    "ضحكتك حلوة",
    "مين مدير الجروب",
    "فاكرني ولا نسيت",
    "يلا نهيص",
    "جيت ازاي النهاردة",
    "احكي لي عن يومك",
    "شفت اللي شفته",
    "انت المشرف هنا",
    "في علاقة حب",
    "كيف حال المساجين",
    "لمحتك امبارح",
    "من اي دولة",
    "انت متصل الآن",
    "انت صديقي",
    "اكلتك المفضلة",
    "ارفعني مشرف بجروبك",
    "انا اسف",
    "تلعب لعبة",
    "صاحبك على ايه",
    "مالك متضايق",
    "عايز شوكولاتة",
    "اهلاً يا سكر",
    "تعال خاص",
    "بتقول حاجة"
]


@app.on_message(filters.command(["تاك", "تاق", "تاك عام"], prefixes=["/", "@", "#", ""]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("هذا الأمر للمجموعات فقط.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("أنت لست مشرفاً يا عزيزي، المشرفين فقط يمكنهم ذلك.")

    if message.reply_to_message and message.text:
        return await message.reply("اكتب (تاك) بجانب الرسالة أو قم بالرد على رسالة لبدء المنشن.")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("اكتب (تاك) بجانب الرسالة أو قم بالرد على رسالة لبدء المنشن.")
    else:
        return await message.reply("اكتب (تاك) بجانب الرسالة أو قم بالرد على رسالة لبدء المنشن.")
    
    if chat_id in spam_chats:
        return await message.reply("يوجد عملية تاك جارية بالفعل، انتظر انتهائها أو أوقفها.")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["منشن", "منشن عام"], prefixes=["/", "@", "#", ""]))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("هذا الأمر للمجموعات فقط.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("أنت لست مشرفاً يا عزيزي، المشرفين فقط يمكنهم ذلك.")
    
    if chat_id in spam_chats:
        return await message.reply("يوجد عملية منشن جارية بالفعل، انتظر انتهائها أو أوقفها.")
    
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["بس", "ايقاف", "الغاء", "cancel"], prefixes=["/", "@", "#", ""]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("لا يوجد منشن شغال حالياً لإيقافه.")
    
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("أنت لست مشرفاً لإيقاف المنشن.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("تم إيقاف المنشن بنجاح.")
