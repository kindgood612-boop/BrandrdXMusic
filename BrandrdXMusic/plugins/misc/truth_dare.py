from pyrogram import filters
import requests
from googletrans import Translator
from BrandrdXMusic import app

# تعريف المترجم
translator = Translator()

# 1. قائمة الكلمات الممنوعة (فلتر القيم الإسلامية)
# أي سؤال يحتوي على هذه الكلمات سيتم حذفه واستبداله فوراً
FORBIDDEN_WORDS = [
    "نبيذ", "بيرة", "كحول", "مشروب", "سكران", "شرب", # كحوليات
    "حبيبتك", "حبيبك", "كراش", "مواعدة", "علاقة", "حب", # علاقات غير شرعية
    "قبلة", "بوسة", "حضن", "شفاه", "فمك", "رقبة", # تلامس
    "عاري", "ملابس داخلية", "اخلع", "جسمك", "صدرك", "فخذ", # عري
    "سرير", "نوم", "جنس", "مثير", "ساخن", "شاذ", "مثلي", # إيحاءات
    "رقص", "ديسكو", "بار", "حظ", "يانصيب" # محرمات أخرى
]

# دالة لجلب وترجمة وفلترة السؤال
def get_safe_content(api_type):
    # الروابط مع تفعيل وضع PG (لتقليل الاحتمالات السيئة من المصدر)
    url = f"https://api.truthordarebot.xyz/v1/{api_type}?rating=pg"
    
    # نحاول 5 مرات البحث عن سؤال نظيف
    for _ in range(5):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                english_text = response.json()["question"]
                
                # ترجمة للعربية
                translated = translator.translate(english_text, dest='ar')
                arabic_text = translated.text
                
                # فحص الرقابة: هل النص يحتوي على كلمات ممنوعة؟
                is_safe = True
                for word in FORBIDDEN_WORDS:
                    if word in arabic_text:
                        is_safe = False
                        break # وجدنا كلمة سيئة، توقف واذهب للمحاولة التالية
                
                # إذا كان السؤال آمناً، أرجعه
                if is_safe:
                    return arabic_text
        except:
            continue
            
    # إذا فشل في إيجاد سؤال نظيف بعد 5 محاولات
    return "تعذر العثور على سؤال مناسب حالياً، حاول مرة أخرى."

@app.on_message(filters.command(["truth", "صراحه", "صراحة"]))
async def get_truth(client, message):
    try:
        # جلب سؤال صراحة آمن
        question = get_safe_content("truth")
        await message.reply_text(question)
    except Exception:
        await message.reply_text("حدث خطأ في الاتصال.")

@app.on_message(filters.command(["dare", "جراه", "جرأة"]))
async def get_dare(client, message):
    try:
        # جلب تحدي جرأة آمن
        dare = get_safe_content("dare")
        await message.reply_text(dare)
    except Exception:
        await message.reply_text("حدث خطأ في الاتصال.")
