from pyrogram import filters
from BrandrdXMusic import app


@app.on_message(filters.command("ping") | filters.regex("^Ping$"))
async def ping_test(_, message):
    await message.reply_text("✅ البوت شغال وبيسمع أوامر")
