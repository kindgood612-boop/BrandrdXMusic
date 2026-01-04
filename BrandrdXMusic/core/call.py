import asyncio
import os
from datetime import datetime, timedelta

from pyrogram import Client
from pyrogram.raw.functions.phone import CreateGroupCall
from pyrogram.errors import ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant

# ==========================================================
# تعديلات PyTgCalls v2.2.9 (النسخة الحديثة بنظام MediaStream)
# ==========================================================
from pytgcalls import PyTgCalls
from pytgcalls.types import Update, MediaStream, AudioQuality, VideoQuality, StreamEnded
from pytgcalls.exceptions import (
    NoActiveGroupCall,
    AlreadyJoinedError,
    NotJoinedError
)

import config
from BrandrdXMusic import LOGGER, app, YouTube
from BrandrdXMusic.misc import db

# ===== Database (CORE STRUCTURE) =====
from BrandrdXMusic.core.database.assistants import group_assistant
from BrandrdXMusic.core.database.settings import (
    get_lang,
    get_loop,
    set_loop,
    is_autoend,
)
from BrandrdXMusic.core.database.queries import set_queries

from BrandrdXMusic.core.database.music import (
    add_active_chat,
    add_active_video_chat,
    remove_active_chat,
    remove_active_video_chat,
    music_on,
)

from BrandrdXMusic.core.exceptions import AssistantErr
from BrandrdXMusic.utils.stream.autoclear import auto_clean
from strings import get_string


# =======================
# Globals
# =======================

AUTOEND = {}
autoend = AUTOEND
QUEUE_LOCK = asyncio.Lock()


# =======================
# Helpers
# =======================

async def _clear_(chat_id: int):
    async with QUEUE_LOCK:
        db[chat_id] = []
    AUTOEND.pop(chat_id, None)
    await remove_active_chat(chat_id)
    await remove_active_video_chat(chat_id)


# =======================
# Call Class (Updated for v2.2.9)
# =======================

class Call:
    def __init__(self):
        # -------- Userbots --------
        self.userbot1 = Client(
            "BrandrdXMusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.userbot2 = Client(
            "BrandrdXMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.userbot3 = Client(
            "BrandrdXMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.userbot4 = Client(
            "BrandrdXMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.userbot5 = Client(
            "BrandrdXMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )

        # -------- PyTgCalls Clients --------
        self.one = PyTgCalls(self.userbot1, cache_duration=100)
        self.two = PyTgCalls(self.userbot2, cache_duration=100)
        self.three = PyTgCalls(self.userbot3, cache_duration=100)
        self.four = PyTgCalls(self.userbot4, cache_duration=100)
        self.five = PyTgCalls(self.userbot5, cache_duration=100)


    # =======================
    # Basic Controls
    # =======================

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.pause_stream(chat_id)
        except:
            pass

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.resume_stream(chat_id)
        except:
            pass

    async def mute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.mute_stream(chat_id)
        except:
            pass

    async def unmute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await assistant.unmute_stream(chat_id)
        except:
            pass

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            # تم التحديث: leave_call بدلاً من leave_group_call
            await assistant.leave_call(chat_id)
        except Exception:
            pass


    # =======================
    # Join Call (v2.2.9 Logic)
    # =======================

    async def join_call(self, chat_id: int, original_chat_id: int, link: str, video: bool = False):
        assistant = await group_assistant(self, chat_id)
        language = await get_lang(chat_id)
        _ = get_string(language)

        if not link.startswith("http") and not os.path.isfile(link):
            raise AssistantErr(_["call_7"])

        # إعداد الـ Stream باستخدام MediaStream
        if video:
            stream = MediaStream(
                link,
                audio_parameters=AudioQuality.HIGH,
                video_parameters=VideoQuality.SD_480p,
            )
        else:
            stream = MediaStream(
                link,
                audio_parameters=AudioQuality.HIGH,
                video_flags=MediaStream.IGNORE,
            )

        try:
            # تم التحديث: play بدلاً من join_group_call
            await assistant.play(
                chat_id,
                stream,
            )

        except NoActiveGroupCall:
            # محاولة الإنشاء يدوياً ثم التشغيل
            try:
                await self.create_call(chat_id)
                await assistant.play(
                    chat_id,
                    stream,
                )
            except Exception:
                raise AssistantErr(_["call_8"])

        except AlreadyJoinedError:
            raise AssistantErr(_["call_9"])
        except Exception as e:
            LOGGER(__name__).error(f"Join Error: {e}")
            raise AssistantErr(_["call_8"])

        await add_active_chat(chat_id)
        await music_on(chat_id)
        await set_queries(1)

        if video:
            await add_active_video_chat(chat_id)

        if await is_autoend():
            asyncio.create_task(self.autoend_watcher(chat_id))

    async def create_call(self, chat_id):
        try:
            await app.invoke(
                CreateGroupCall(
                    peer=await app.resolve_peer(chat_id),
                    random_id=app.rnd_id(),
                )
            )
        except:
            pass

    # =======================
    # Change Stream (v2.2.9 Logic)
    # =======================

    async def change_stream(self, client: PyTgCalls, chat_id: int):
        async with QUEUE_LOCK:
            queue = db.get(chat_id)
            if not queue:
                await self.stop_stream(chat_id)
                return

            loop_count = await get_loop(chat_id)
            popped = queue.pop(0) if loop_count == 0 else None
            if loop_count > 0:
                await set_loop(chat_id, loop_count - 1)

        await auto_clean(popped)

        async with QUEUE_LOCK:
            if not db.get(chat_id):
                await self.stop_stream(chat_id)
                return
            data = db[chat_id][0]

        file = data["file"]
        videoid = data["vidid"]
        streamtype = data["streamtype"]

        link = await YouTube.video(videoid, file.startswith("live_")) if file.startswith(("vid_", "live_")) else file

        if not link.startswith("http") and not os.path.isfile(link):
            await self.stop_stream(chat_id)
            return

        # إعداد الـ Stream
        if streamtype == "video":
            stream = MediaStream(
                link,
                audio_parameters=AudioQuality.HIGH,
                video_parameters=VideoQuality.SD_480p,
            )
        else:
            stream = MediaStream(
                link,
                audio_parameters=AudioQuality.HIGH,
                video_flags=MediaStream.IGNORE,
            )

        try:
            # تم التحديث: play
            await client.play(
                chat_id,
                stream,
            )
        except Exception as e:
            LOGGER(__name__).error(e)
            await self.stop_stream(chat_id)


    # =======================
    # Auto-End Watcher
    # =======================

    async def autoend_watcher(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        AUTOEND[chat_id] = datetime.now() + timedelta(minutes=1)

        while True:
            await asyncio.sleep(20)

            if chat_id not in AUTOEND:
                return

            if datetime.now() < AUTOEND[chat_id]:
                continue

            try:
                participants = await assistant.get_participants(chat_id)
            except Exception:
                continue

            if len(participants) <= 1:
                await self.stop_stream(chat_id)
                AUTOEND.pop(chat_id, None)
                return


    # =======================
    # Start & Decorators (v2.2.9 Logic)
    # =======================

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Clients (v2.2.9)...")

        for idx, client in enumerate(
            [self.one, self.two, self.three, self.four, self.five], start=1
        ):
            try:
                await client.start()
                LOGGER(__name__).info(f"✅ Assistant {idx} started")
            except Exception as e:
                LOGGER(__name__).warning(f"⚠️ Assistant {idx} skipped: {e}")

    async def decorators(self):
        for client in [self.one, self.two, self.three, self.four, self.five]:
            # تم التحديث: استخدام on_update و StreamEnded
            @client.on_update()
            async def _(c, update: Update):
                if isinstance(update, StreamEnded):
                    try:
                        await self.change_stream(c, update.chat_id)
                    except:
                        pass


# =======================
# Instance
# =======================

Hotty = Call()
