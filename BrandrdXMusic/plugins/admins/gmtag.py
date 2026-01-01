from BrandrdXMusic import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

# تم تبسيط الإيموجي ليكون رمزاً واحداً أو اثنين فقط
EMOJI = [ "🦋", "🌸", "🌹", "🍬", "⚡️", "✨", "🎈", "🧸", "🤍", "🌿", "🍉", "🍓", "☕️", "☁️", "💜", "🪴", "🐬", "🦄", "🌙", "💤" ]

# رسائل الليل (نص عادي بدون زخرفة عريضة)
TAGMES = [ 
    "تصبح على خير يا غالي",
    "نام وارتاح، وراك يوم طويل",
    "سيب الجوال ونام عشان صحتك",
    "أحلام سعيدة يا قمر",
    "تصبحوا على واقع أجمل",
    "كفاية سهر بقى وناموا",
    "نوم العوافي يا رب",
    "طفي النت ونام",
    "يا رب تصحى على خبر حلو",
    "هدوء الليل جميل، تصبح على خير",
    "غطى نفسك كويس الجو برد",
    "استغفر ونام",
    "تصبح على خير، لا تنسى الأذكار",
    "يلا نوم، الشاحن ارتاح وانت لسه",
    "نوم الهنا والسرور",
    "بكره يوم جديد، نام عشان تركز",
    "تصبح على حب وسعادة",
    "روح نام يا سكر",
    "السرير يناديك",
    "تصبح على خير يا صديقي",
    "نوم عميق وأحلام وردية",
    "يلا قدامي على النوم",
    "تصبحون على ما تتمنون",
    "حان وقت النوم، تصبحوا على خير",
    "صحة وعافية، نوم سعيد"
]

# رسائل الصباح (نص عادي بدون زخرفة عريضة)
VC_TAG = [
    "صباح الخير يا جميل",
    "قوم اصحى الشمس طلعت",
    "صباح النشاط والحيوية",
    "يومك سعيد إن شاء الله",
    "اصحى وفوق كدا، ورانا شغل",
    "صباح الورد والياسمين",
    "تعال اشرب قهوة معنا",
    "صباحك عسل يا عسل",
    "يلا اصحى كفاية نوم",
    "صباح الخير، كيف أصبحت؟",
    "بداية يوم جديد، تفاءل",
    "اصحى يا كسول",
    "فطورك جاهز ولا لسه",
    "صباح الرضا من الرحمن",
    "صباح الفل والياسمين",
    "قوم غسل وشك وفوق",
    "يا فتاح يا عليم، صباح الخير",
    "منور الصباح بوجودك",
    "صباحك سكر زيادة",
    "يوم موفق لك يا غالي",
    "أحلى صباح لأحلى ناس",
    "اصحى الدنيا بتناديك",
    "صباح الأمل والتفاؤل",
    "قهوتك جاهزة؟ صباح الخير"
]


@app.on_message(filters.command(["تاك نوم", "نوم", "تصبحون"], prefixes=["/", "@", "#", ""]))
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
        return await message.reply("اكتب (تاك نوم) لبدء المنشن الليلي.")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("اكتب (تاك نوم) لبدء المنشن الليلي.")
    else:
        return await message.reply("اكتب (تاك نوم) لبدء المنشن الليلي.")
    
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
                # رسالة عادية بدون تغليظ
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


@app.on_message(filters.command(["تاك صباح", "صباح", "قوموا"], prefixes=["/", "@", "#", ""]))
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
            # رسالة عادية بدون تغليظ
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["ايقاف", "بس", "الغاء", "cancel"], prefixes=["/", "@", "#", ""]))
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
