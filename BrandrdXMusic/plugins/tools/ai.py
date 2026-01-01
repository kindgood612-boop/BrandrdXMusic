import g4f
import random
import asyncio
from pyrogram import filters, enums
from BrandrdXMusic import app

# --- إعدادات المكتبة ---
g4f.debug.logging = False

# --- دالة إضافة الكاشيدة (التطويل) للنص العربي ---
def style_text(text):
    if not text:
        return ""
    
    # الحروف التي لا يجوز وضع كاشيدة بعدها (الحروف الرافسة + المسافات)
    forbidden_after = "اأإآدذرزوؤةء "
    
    result = ""
    for i, char in enumerate(text):
        result += char
        
        # شروط إضافة الكاشيدة:
        # 1. الحرف عربي
        # 2. الحرف ليس في نهاية النص
        # 3. الحرف ليس من الحروف الرافسة (forbidden_after)
        # 4. الحرف الذي يليه ليس مسافة (نهاية الكلمة)
        # 5. نسبة عشوائية (70%) حتى لا يكون النص طويلاً جداً ومملاً
        if (i < len(text) - 1 and
            "\u0600" <= char <= "\u06FF" and
            char not in forbidden_after and
            text[i+1] != " " and
            random.randint(0, 100) < 70):
            
            result += "ـ"
            
    return result

# --- دالة الإيموجي (نظام 1 من 3) ---
def get_emoji():
    # اختيار رقم عشوائي من 1 إلى 3
    # إذا كان الرقم 1، نرجع إيموجي، غير ذلك نرجع نص فارغ
    if random.randint(1, 3) == 1:
        return f" {random.choice(['🤍', '🧚'])}"
    return ""

# --- معالج الأوامر (الأوامر بدون كاشيدة كما طلبت) ---
@app.on_message(filters.command(["gpt", "ai", "ask", "سؤال", "ذكاء"]))
async def smart_ai(client, message):
    try:
        # التأكد من وجود سؤال
        if len(message.command) < 2:
            reply = style_text("اكتب سؤالك بجانب الامر")
            await message.reply_text(f"**{reply}..** 🤍", quote=True)
            return

        query = message.text.split(None, 1)[1]
        
        # إرسال "جاري الكتابة"
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        
        # رسالة الانتظار (أيضاً مزخرفة)
        wait_msg = await message.reply_text(f"**{style_text('جاري التفكير')}...**", quote=True)

        # الاتصال بـ GPT-4
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومفيد. اجعل إجاباتك مختصرة وذكية."},
                {"role": "user", "content": query}
            ],
        )

        # تنسيق الرد النهائي
        if response:
            # 1. تنظيف الرد الخام
            clean_reply = response.strip()
            
            # 2. إضافة الكاشيدة (التطويل) على الرد
            stylized_reply = style_text(clean_reply)
            
            # 3. إضافة الإيموجي (حسب الحظ)
            emoji = get_emoji()
            
            # إرسال الرد
            await wait_msg.edit(
                f"**{stylized_reply}**{emoji}",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await wait_msg.edit(style_text("حدث خطأ حاول مرة اخرى"))

    except Exception as e:
        print(f"AI Error: {e}")
        try:
            # محاولة احتياطية بموديل آخر
            response_backup = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": query}],
            )
            if response_backup:
                final_bk = style_text(response_backup)
                await wait_msg.edit(f"**{final_bk}** 🧚")
            else:
                await wait_msg.edit(style_text("الخوادم مشغولة الان"))
        except:
            pass
