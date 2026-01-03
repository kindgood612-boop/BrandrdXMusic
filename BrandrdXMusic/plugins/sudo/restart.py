import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

import config
from BrandrdXMusic import app
from BrandrdXMusic.misc import HAPP, SUDOERS, XCB

# [CORE MIGRATION] استيراد دوال قاعدة البيانات
from BrandrdXMusic.core.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from BrandrdXMusic.utils.pastebin import HottyBin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()


# ==========================================================
# 1. أوامر جلب السجل (Logs)
# ==========================================================
@app.on_message(filters.command(["getlog", "logs", "getlogs", "السجل", "سجل"], prefixes=["", "/", "!", ".", "@", "#"]) & SUDOERS)
async def log_(client, message):
    try:
        if os.path.exists("log.txt"):
            await message.reply_document(
                document="log.txt",
                caption="🧚 **تـفـضـل مـلـف الـسـجـلات (Logs) الـخـاص بـالـبـوت...**"
            )
        else:
            await message.reply_text("🥀 **لا يـوجـد مـلـف سـجـلات حـالـيـاً.**")
    except:
        await message.reply_text("🥀 **عـذراً، حـدث خـطـأ أثـنـاء جـلـب الـسـجـلات.**")


# ==========================================================
# 2. أوامر التحديث (Update)
# ==========================================================
@app.on_message(filters.command(["update", "gitpull", "تحديث", "التحديث"], prefixes=["", "/", "!", ".", "@", "#"]) & SUDOERS)
async def update_(client, message):
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text("🥀 **يـرجـى الـتـحـقـق مـن مـتـغـيـر `HEROKU_APP_NAME` أولاً.**")
    
    response = await message.reply_text("🧚 **جـارٍ الـبـحـث عـن تـحـديـثـات جـديـدة...**")
    
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("🥀 **حـدث خـطـأ فـي Git Command.**")
    except InvalidGitRepositoryError:
        return await response.edit("🥀 **مـجـلـد الـريـبـو غـيـر صـالـح.**")
        
    to_exc = f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    
    verification = ""
    # ملاحظة: تم تعديل طريقة الحصول على الرابط لتفادي الأخطاء المحتملة
    REPO_ = repo.remotes.origin.url.split(".git")[0]
    
    for checks in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        verification = str(checks.count())
        
    if verification == "":
        return await response.edit("🧚 **الـبـوت مـحـدث بـالـفـعـل عـلـى آخـر إصـدار !**")
        
    updates = ""
    # دالة لتنسيق التاريخ (1st, 2nd, etc.)
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    
    for info in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> ʙʏ -> {info.author}</b>\n\t\t\t\t<b>➥ ᴄᴏᴍᴍɪᴛᴇᴅ ᴏɴ :</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    
    _update_response_ = "🧚 **يـوجـد تـحـديـث جـديـد لـلـبـوت !**\n\n🥀 **يـتـم الآن سـحـب الـتـحـديـثـات...**\n\n<b><u>الـتـغـيـيـرات :</u></b>\n\n"
    _final_updates_ = _update_response_ + updates
    
    if len(_final_updates_) > 4096:
        url = await HottyBin(updates)
        nrs = await response.edit(
            f"🧚 **يـوجـد تـحـديـث جـديـد لـلـبـوت !**\n\n🥀 **يـتـم الآن سـحـب الـتـحـديـثـات...**\n\n<u><b>الـتـغـيـيـرات :</b></u>\n\n<a href={url}>اضـغـط هـنـا لـرؤيـة الـتـحـديـثـات</a>"
        )
    else:
        nrs = await response.edit(_final_updates_, disable_web_page_preview=True)
        
    os.system("git stash &> /dev/null && git pull")

    # إشعار المجموعات النشطة بالتحديث
    try:
        served_chats = await get_active_chats()
        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text="🥀 **تـم تـحـديـث الـبـوت... سـنـعـود لـلـعـمـل خـلال دقـائـق.**\n🧚 {0}".format(app.mention),
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except:
                pass
        await response.edit(f"{nrs.text}\n\n🧚 **تـم سـحـب الـتـحـديـثـات، جـارٍ إعـادة الـتـشـغـيـل...**")
    except:
        pass

    if await is_heroku():
        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(f"{nrs.text}\n\n🥀 **حـدث خـطـأ أثـنـاء إعـادة الـتـشـغـيـل عـلـى هـيـروكـو.**")
            return await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"Error: {err}",
            )
    else:
        os.system("pip3 install -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && bash start")
        exit()


# ==========================================================
# 3. أوامر إعادة التشغيل (Restart)
# ==========================================================
@app.on_message(filters.command(["restart", "اعادة تشغيل", "إعادة تشغيل"], prefixes=["", "/", "!", ".", "@", "#"]) & SUDOERS)
async def restart_(_, message):
    response = await message.reply_text("🥀 **جـارٍ إعـادة الـتـشـغـيـل...**")
    
    ac_chats = await get_active_chats()
    for x in ac_chats:
        try:
            await app.send_message(
                chat_id=int(x),
                text=f"🧚 **يـتـم إعـادة تـشـغـيـل الـبـوت...**\n🥀 **يـمـكـنـك الـتـشـغـيـل مـجـدداً بـعـد 20 ثـانـيـة.**\n✨ {app.mention}",
            )
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except:
            pass

    try:
        shutil.rmtree("downloads")
        shutil.rmtree("raw_files")
        shutil.rmtree("cache")
    except:
        pass
        
    await response.edit_text(
        "🧚 **تـم بـدء عـمـلـيـة إعـادة الـتـشـغـيـل، انـتـظـر قـلـيـلاً حـتـى يـعـود الـبـوت لـلـعـمـل...**"
    )
    os.system(f"kill -9 {os.getpid()} && bash start")
