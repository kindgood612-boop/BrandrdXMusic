from pyrogram import filters
from BrandrdXMusic import app

@app.on_message(filters.all)
async def force_handler(_, message):
    try:
        text = message.text or ""

        if text.startswith(("/", "!", ".")):
            await message.reply_text(
                f"✅ الأمر وصل\n\n"
                f"📌 النص: `{text}`\n"
                f"📍 المكان: {'خاص' if message.chat.type == 'private' else 'جروب'}"
            )
    except Exception as e:
        print(e)
