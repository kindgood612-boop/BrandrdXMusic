import os
import socket
import requests
import yt_dlp
from urllib.parse import urlparse
from pyrogram import filters
from BrandrdXMusic import app

# --- إعدادات الكوكيز ---
COOKIE_LINK = "https://batbin.me/raw/koumyss"

# --- أوامر التحميل ---
COMMANDS = ["ig", "instagram", "reel", "انستا", "ريلز"]

# --- دالة إصلاح الاتصال (DNS Bypass) ---
def fix_dns_for_url(url):
    try:
        domain = urlparse(url).netloc
        doh_url = f"https://dns.google/resolve?name={domain}&type=A"
        resp = requests.get(doh_url, timeout=5).json()
        if 'Answer' in resp:
            real_ip = resp['Answer'][0]['data']
            orig_addr = socket.getaddrinfo
            def patched_addr(host, *args, **kwargs):
                if host == domain:
                    return orig_addr(real_ip, *args, **kwargs)
                return orig_addr(host, *args, **kwargs)
            socket.getaddrinfo = patched_addr
            return True
    except:
        pass
    return False

@app.on_message(filters.command(COMMANDS))
async def download_instagram_video(client, message):
    try:
        # 1. التحقق من مكان الرابط
        if message.reply_to_message and message.reply_to_message.text:
            url = message.reply_to_message.text
        elif len(message.command) > 1:
            url = message.text.split(None, 1)[1]
        else:
            await message.reply_text("**يـرجـى وضـع الـرابـط بـعـد الأمـر أو الـرد عـلى الـرابـط.**")
            return

        # رسالة المعالجة (بدون إيموجي)
        status_msg = await message.reply_text("**جـاري الـمـعـالـجـة...**")

        user_id = message.from_user.id
        
        # 2. إصلاح الاتصال وجلب الكوكيز
        fix_dns_for_url(COOKIE_LINK)
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = requests.get(COOKIE_LINK, headers=headers, timeout=15)
        
        if req.status_code != 200:
            await status_msg.edit("**فـشـل الـاتـصـال بـمـلـف الـكـوكـيـز.**")
            return

        # حفظ الكوكيز مؤقتاً
        cookie_file = f"cookies_{user_id}.txt"
        with open(cookie_file, "w", encoding="utf-8") as f:
            f.write(req.text)

        # 3. إعدادات التحميل (ضمان الصوت والصورة)
        ydl_opts = {
            'format': 'best[vcodec^=avc1][acodec!=none]/best[acodec!=none]/best',
            'outtmpl': f'insta_{user_id}_%(id)s.%(ext)s',
            'cookiefile': cookie_file,
            'geo_bypass': True,
            'quiet': True,
            'noplaylist': True,
            'ignoreerrors': True,
        }

        path = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = ydl.prepare_filename(info)
                
                # التحقق من وجود الملف
                if not os.path.exists(path):
                    base, ext = os.path.splitext(path)
                    for f in os.listdir('.'):
                        if f.startswith(base):
                            path = f
                            break
        except Exception as e:
            print(f"Error: {e}")

        # 4. إرسال الفيديو وتنظيف الملفات
        if path and os.path.exists(path):
            await status_msg.delete()
            await client.send_video(
                chat_id=message.chat.id,
                video=path,
                caption=f"🤍 **تـم الـتـحـمـيـل بـواسـطـة :** {client.me.mention}",
                reply_to_message_id=message.id
            )
            os.remove(path)
        else:
            await status_msg.edit("**تـعـذر الـتـحـمـيـل، تـأكـد مـن صـحـة الـرابـط.**")

        # حذف ملف الكوكيز
        if os.path.exists(cookie_file):
            os.remove(cookie_file)

    except Exception as e:
        print(f"Handler Error: {e}")
        try:
            await status_msg.edit("**حـدث خـطـأ أثـنـاء الـتـحـمـيـل.**")
        except:
            pass
