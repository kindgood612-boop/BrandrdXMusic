import os
import re
import random
import aiofiles
import aiohttp
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ImageChops
from youtubesearchpython.__future__ import VideosSearch
from BrandrdXMusic import app
from config import YOUTUBE_IMG_URL

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Helper Functions (أدوات الرسم الذكية)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text, limit):
    if len(text) <= limit:
        return text
    text = text[:limit]
    return text.rsplit(' ', 1)[0] + "..."

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def get_dominant_color(pil_img):
    img = pil_img.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    dominant_color = img.getpixel((0, 0))
    return dominant_color

def create_reflection(im, opacity=60):
    # إنشاء انعكاس للصورة (مثل المرآة)
    reflection = ImageOps.flip(im)
    reflection = reflection.convert("RGBA")
    
    # إنشاء قناع تدرج شفاف (Gradient Mask)
    w, h = im.size
    gradient = Image.new('L', (1, h), color=0xFF)
    for y in range(h):
        # التدرج من الشفافية إلى الاختفاء
        gradient.putpixel((0, y), int(255 * (1 - y / h) * (opacity / 100)))
    
    alpha = gradient.resize((w, h))
    reflection.putalpha(alpha)
    return reflection

def draw_waveform(draw, x_start, y_base, width, color):
    # رسم موجات صوتية وهمية
    bar_width = 8
    spacing = 4
    num_bars = width // (bar_width + spacing)
    
    for i in range(int(num_bars)):
        # ارتفاع عشوائي يعطي شكل الموجة
        height = random.randint(10, 60)
        # جعل الموجات في المنتصف أطول
        if i > num_bars // 3 and i < 2 * (num_bars // 3):
            height += random.randint(10, 30)
            
        x = x_start + i * (bar_width + spacing)
        y1 = y_base - height
        y2 = y_base
        
        draw.rounded_rectangle([(x, y1), (x + bar_width, y2)], radius=3, fill=color)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Main Logic (المعالجة الرئيسية)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        # ━━━ التصميم العبقري (Genius Design) ━━━
        
        youtube = Image.open(f"cache/thumb{videoid}.png")
        dom_color = get_dominant_color(youtube) # اللون الأساسي
        
        # 1. الخلفية السينمائية
        background = changeImageSize(1280, 720, youtube)
        background = background.filter(ImageFilter.GaussianBlur(40)) # تغبيش عالي جداً
        
        # تدرج أسود (Vignette) لتركيز النظر في المنتصف
        dark_layer = Image.new("RGBA", (1280, 720), (0,0,0,0))
        draw_dark = ImageDraw.Draw(dark_layer)
        # رسم تدرج من الأسفل للأعلى (لجعل النصوص واضحة)
        for y in range(720):
            alpha = int((y / 720) * 180) # تدرج الشفافية
            draw_dark.line([(0, y), (1280, y)], fill=(0, 0, 0, alpha))
        
        background.paste(dark_layer, (0,0), dark_layer)

        # 2. تجهيز صورة الألبوم (Art Work)
        art_size = 420
        art = changeImageSize(1280, 720, youtube)
        art = art.crop((280, 0, 1000, 720)) 
        art = art.resize((art_size, art_size))
        art = art.convert("RGBA")
        art = add_corners(art, 25)

        # 3. توهج خلف الصورة (Glow Effect)
        glow = Image.new("RGBA", (art_size + 80, art_size + 80), dom_color)
        glow = add_corners(glow, 40)
        glow = glow.filter(ImageFilter.GaussianBlur(40)) # توهج ناعم
        
        # 4. الانعكاس (Reflection)
        reflection = create_reflection(art)

        # دمج العناصر: التوهج -> الصورة -> الانعكاس
        center_x = 430
        center_y = 60
        
        background.paste(glow, (center_x - 40, center_y - 40), glow) # التوهج خلف الصورة
        background.paste(art, (center_x, center_y), art) # الصورة الأصلية
        background.paste(reflection, (center_x, center_y + art_size + 5), reflection) # الانعكاس أسفل الصورة

        draw = ImageDraw.Draw(background)

        # 5. الخطوط
        try:
            font_title = ImageFont.truetype("BrandrdXMusic/assets/font.ttf", 45)
            font_light = ImageFont.truetype("BrandrdXMusic/assets/font2.ttf", 28)
            font_small = ImageFont.truetype("BrandrdXMusic/assets/font2.ttf", 22)
        except:
            font_title = ImageFont.load_default()
            font_light = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # 6. النصوص والمعلومات
        # العنوان في المنتصف السفلي
        clean_title = truncate(title, 40)
        
        # رسم ظل للنص (للوضوح التام)
        draw.text((642, 532), clean_title, fill="black", font=font_title, anchor="mm")
        draw.text((640, 530), clean_title, fill="white", font=font_title, anchor="mm")
        
        # القناة
        draw.text((640, 580), channel, fill=(200, 200, 200), font=font_light, anchor="mm")

        # 7. رسم الموجات الصوتية (Waveform Visualizer)
        # نرسمها أسفل العنوان وفوق شريط الوقت
        draw_waveform(draw, x_start=340, y_base=630, width=600, color=dom_color)

        # 8. شريط الوقت والبيانات
        # أيقونات بسيطة (رموز نصية)
        draw.text((300, 650), "🥀 " + views, fill="white", font=font_small, anchor="lm")
        draw.text((980, 650), "💕 " + duration, fill="white", font=font_small, anchor="rm")
        
        # خط فاصل بسيط
        draw.line([(340, 675), (940, 675)], fill=(255, 255, 255, 50), width=1)
        draw.line([(340, 675), (540, 675)], fill=dom_color, width=3) # الجزء المكتمل من الخط

        # الحفظ
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
            
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print(f"Genius Thumbnail Error: {e}")
        return YOUTUBE_IMG_URL
