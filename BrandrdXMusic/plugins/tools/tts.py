import io

from gtts import gTTS
from pyrogram import filters

from BrandrdXMusic import app


@app.on_message(
    filters.command(
        ["tts", "نطق", "قول", "انطق"],
        prefixes=["/", "!", ".", ""]
    )
)
async def text_to_speech(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "🥀 **يرجى كتابة النص المراد تحويله لصوت بجوار الأمر.**"
        )

    text = message.text.split(None, 1)[1]
    # تم تغيير اللغة إلى العربية (ar) بدلاً من الهندية
    tts = gTTS(text, lang="ar") 
    audio_data = io.BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)

    audio_file = io.BytesIO(audio_data.read())
    audio_file.name = "audio.mp3"
    await message.reply_audio(audio_file)


__HELP__ = """
**تحويل النص الى صوت**

استخدم هذه الأوامر لتحويل الكتابة إلى ملف صوتي مسموع:

- نطق [النص] : سيقوم البوت بنطق الكلام المكتوب.
- قول [النص] : نفس الأمر.

**مثال:**
- نطق السلام عليكم
"""

__MODULE__ = "النطق"
