from BrandrdXMusic import app
import asyncio
import random
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant

spam_chats = []

SHAYRI = [
    "ألا يا قلبُ صبراً لا تُطِلْ جزَعــا\nفكم في الصبرِ من فَرَجٍ لمن صَبَرا",
    "إذا ضاقتْ بكَ الدنيا بما رحُبَتْ\nفاعلمْ بأنَّ مع العُسرِ يُســرا",
    "وما الحزنُ إلا سحابةٌ عَبَرَتْ\nستنجلي، ويعودُ القلبُ مُزدهِرا",
    "تأنَّ ولا تيأسْ إذا جارَ الزمـانُ\nفكم بعدَ العَنا فُتِحَتْ لنا الدُّرَرُ",
    "نُخبِّئُ في الصدورِ وجعَ الليالي\nويحسبُنا الورى أنا لا نُكابِدُ",
    "صديقُ النفسِ مَن إن ضاقَ يومُك\nأتاك بغيرِ وعدٍ يُسانِدُ",
    "سلامٌ على قلبٍ تحمّلَ صامتاً\nولم يشكُ يوماً رغم ثقلِ الأسى",
    "تُعلِّمُنا الحياةُ وليس نَدري\nبأن الصبرَ بابُ المُستراحِ",
    "إذا انكسرَ الفؤادُ فلا تُرِهْ\nفبعضُ الكسرِ يُخفى لا يُقالُ",
    "وما الدنيا بدارِ خلودٍ\nولكنها ممرٌّ وابتلاءُ",

    # -------- 40 بيت إضافي --------

    "ومن يجعلِ المعروفَ في غيرِ أهلِه\nيكن حمدُه ذمّاً عليه ويَندمِ",
    "دعِ الأيامَ تفعلُ ما تشـاءُ\nوطِبْ نفساً إذا حكمَ القضاءُ",
    "إذا المرءُ لم يدنسْ من اللؤمِ عرضُه\nفكلُّ رداءٍ يرتديه جميلُ",
    "وما نيلُ المطالبِ بالتمنّي\nولكن تُؤخذُ الدنيا غِلابا",
    "لا تحسبنَّ المجدَ تمراً أنتَ آكلُه\nلن تبلغَ المجدَ حتى تلعقَ الصَّبرا",
    "ومن لم يذُق مُرَّ التعلُّمِ ساعةً\nتجرّعَ ذلَّ الجهلِ طولَ حياتِه",
    "على قدرِ أهلِ العزمِ تأتي العزائمُ\nوتأتي على قدرِ الكرامِ المكارمُ",
    "ليس الجمالُ بأثوابٍ تُزيّنُنا\nإن الجمالَ جمالُ العلمِ والأدبِ",
    "وإذا كانتِ النفوسُ كباراً\nتعبتْ في مرادِها الأجسامُ",
    "ربَّ أخٍ لك لم تلدهُ أمُّك",
    "كن كالنخيلِ عن الأحقادِ مرتفعاً\nيُرمى بصخرٍ فيُلقي أطيبَ الثمرِ",

    "إذا ما كنتَ ذا قلبٍ قنوعٍ\nفأنتَ ومالكُ الدنيا سواءُ",
    "ولا خيرَ في ودٍّ إذا لم يكن له\nعلى حرِّ نارِ الامتحانِ ثبوتُ",
    "وما كلُّ برقٍ لاحَ لي يستفزُّني\nولا كلُّ من في الأرضِ أرضاهُ صاحبا",
    "سيذكرني قومي إذا جدَّ جدُّهم\nوفي الليلةِ الظلماءِ يُفتقدُ البدرُ",
    "ومن يصنعِ المعروفَ لا يعدمْ جوازِيَه\nلا يذهبُ العُرفُ بين اللهِ والناسِ",
    "إذا غامرتَ في شرفٍ مرومِ\nفلا تقنعْ بما دونَ النجومِ",
    "ومن يتهيبْ صعودَ الجبالِ\nيعشْ أبدَ الدهرِ بين الحُفَرِ",
    "ولربَّ نازلةٍ يضيقُ بها الفتى\nذرعاً وعندَ اللهِ منها المخرجُ",
    "وما التأنيثُ لاسمِ الشمسِ عيبٌ\nولا التذكيرُ فخرٌ للهلالِ",
    "لا تنهَ عن خُلُقٍ وتأتيَ مثلَه\nعارٌ عليكَ إذا فعلتَ عظيمُ",

    "وكن رجلاً إذا أتوا بعدَه\nيقولون مرَّ وهذا الأثرُ",
    "ولا تَحسبَنَّ اللهَ يُغفلُ ساعةً\nولا أنَّ ما تُخفي عليه يَغيبُ",
    "إذا المرءُ أكرمَ نفسَهُ أكرمَهُ الورى",
    "وخيرُ جليسٍ في الزمانِ كتابُ",
    "وليسَ الغنى عن كثرةِ المالِ إنما\nغنى النفسِ أن ترضى بما هو كائنُ",
    "ومن يثقِ الدنيا يكن مثلَ قابضٍ\nعلى الماءِ خانتْهُ فُروجُ الأصابعِ"
]


@app.on_message(
    filters.command(
        ["shayari", "شعر", "قصيد", "بوح"],
        prefixes=["/", "@", "#", ""]
    )
    & filters.group
)
async def shayari_handler(client, message):
    chat_id = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("هذا الأمر يعمل في المجموعات فقط.")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return await message.reply_text("هذا الأمر مخصّص للمشرفين فقط.")
    except UserNotParticipant:
        return await message.reply_text("لا يمكنك استخدام هذا الأمر.")

    if chat_id in spam_chats:
        return await message.reply_text("يوجد شعر يُرسل حالياً، انتظر حتى ينتهي.")

    spam_chats.append(chat_id)

    try:
        async for member in client.get_chat_members(chat_id):
            if chat_id not in spam_chats:
                break
            if member.user.is_bot:
                continue

            text = (
                f"<a href='tg://user?id={member.user.id}'>{member.user.first_name}</a>\n\n"
                f"{random.choice(SHAYRI)}"
            )

            await client.send_message(chat_id, text, disable_web_page_preview=True)
            await asyncio.sleep(4)

    finally:
        if chat_id in spam_chats:
            spam_chats.remove(chat_id)


@app.on_message(
    filters.command(
        ["cancelshayari", "shayarioff", "بس شعر", "ايقاف شعر"],
        prefixes=["/", "@", "#", ""]
    )
    & filters.group
)
async def cancel_shayari(client, message):
    chat_id = message.chat.id

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return await message.reply_text("فقط المشرف يمكنه إيقاف الشعر.")
    except UserNotParticipant:
        return await message.reply_text("لا يمكنك إيقاف الأمر.")

    if chat_id not in spam_chats:
        return await message.reply_text("لا يوجد شعر يعمل حالياً.")

    spam_chats.remove(chat_id)
    await message.reply_text("تم إيقاف الشعر بنجاح.")
