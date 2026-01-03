import asyncio
import os
import re
from typing import Union, Optional, Tuple
import yt_dlp
import aiohttp
import aiofiles
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from BrandrdXMusic.utils.formatters import time_to_seconds
from BrandrdXMusic import LOGGER

# --- إعدادات المجلد ---
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# --- إعدادات الـ API ---
YOUR_API_URL: Optional[str] = None
FALLBACK_API_URL = "https://shrutibots.site"


async def load_api_url():
    """
    يحاول حفظ رابط API من مصدر خارجي (pastebin) وإلا يستخدم fallback.
    """
    global YOUR_API_URL
    logger = LOGGER("BrandrdXMusic.platforms.Youtube.py")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://pastebin.com/raw/rLsBhAQa", timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    content = await response.text()
                    YOUR_API_URL = content.strip()
                    logger.info("API URL loaded successfully")
                else:
                    YOUR_API_URL = FALLBACK_API_URL
                    logger.info("Using fallback API URL (Status != 200)")
    except Exception as e:
        YOUR_API_URL = FALLBACK_API_URL
        logger.info(f"Using fallback API URL (Exception): {e}")


# تشغيل دالة تحميل الـ API عند بدء التشغيل (غير حاسم إن فشل)
try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(load_api_url())
    else:
        loop.run_until_complete(load_api_url())
except RuntimeError:
    # في بيئات معينة لا يمكن الحصول على loop، سنتجاهل لأنه غير حاسم
    pass


# ======================
# دوال ytdlp (تعمل في thread عشان لا توقف الـ event loop)
# ======================

def _run_ytdlp_extract(link: str, ydl_opts: dict) -> Optional[dict]:
    """
    دالة تزامنية لتشغيل yt_dlp واستخراج المعلومات (تُستدعى عبر asyncio.to_thread).
    ترجع dict المعلومات أو None.
    """
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            return info
    except Exception:
        return None


async def download_song_ytdlp(link: str) -> Optional[str]:
    """
    تحميل صوتي باستخدام yt-dlp محلياً. يعيد مسار الملف أو None.
    """
    logger = LOGGER(__name__)
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        info = await asyncio.to_thread(_run_ytdlp_extract, link, ydl_opts)
        if not info:
            logger.error("yt-dlp audio: no info returned")
            return None

        video_id = info.get("id")
        if not video_id:
            logger.error("yt-dlp audio: no id in info")
            return None

        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
        if os.path.exists(file_path):
            return file_path
        # In rare cases extension could be different; fallback scan
        for ext in ("mp3", "m4a", "webm", "opus"):
            alt = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
            if os.path.exists(alt):
                return alt
        return None

    except Exception as e:
        LOGGER(__name__).error(f"yt-dlp audio error: {e}")
        return None


async def download_video_ytdlp(link: str) -> Optional[str]:
    """
    تحميل فيديو باستخدام yt-dlp محلياً. يعيد مسار الملف أو None.
    """
    logger = LOGGER(__name__)
    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": f"{DOWNLOAD_DIR}/%(id)s.%(ext)s",
            "quiet": True,
            "no_warnings": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "merge_output_format": "mp4",
        }

        info = await asyncio.to_thread(_run_ytdlp_extract, link, ydl_opts)
        if not info:
            logger.error("yt-dlp video: no info returned")
            return None

        video_id = info.get("id")
        ext = info.get("ext", "mp4") or "mp4"
        if not video_id:
            logger.error("yt-dlp video: no id in info")
            return None

        file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.{ext}")
        if os.path.exists(file_path):
            return file_path
        # fallback scan for common extensions
        for alt_ext in ("mp4", "mkv", "webm", "m4a"):
            alt = os.path.join(DOWNLOAD_DIR, f"{video_id}.{alt_ext}")
            if os.path.exists(alt):
                return alt
        return None

    except Exception as e:
        LOGGER(__name__).error(f"yt-dlp video error: {e}")
        return None


# ======================
# تحميل عبر API ثم fallback محلي
# ======================

async def _write_stream_to_file(stream, file_path: str):
    """
    يكتب استجابة aiohttp إلى ملف باستخدام aiofiles.
    """
    async with aiofiles.open(file_path, "wb") as f:
        async for chunk in stream.iter_chunked(16384):
            if not chunk:
                continue
            await f.write(chunk)


async def download_song(link: str) -> Optional[str]:
    """
    يحاول أولاً تحميل المسار عبر الـ API (إذا متوفر)، وإلا fallback إلى yt-dlp محلي.
    يعيد مسار الملف أو None.
    """
    global YOUR_API_URL
    logger = LOGGER(__name__)

    if not YOUR_API_URL:
        await load_api_url()
        if not YOUR_API_URL:
            YOUR_API_URL = FALLBACK_API_URL

    # الحصول على Id من رابط يوتيوب إن أمكن
    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link

    if not video_id or len(video_id) < 3:
        # رابط غير قياسي -> استخدم yt-dlp محلي فورًا
        return await download_song_ytdlp(link)

    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp3")
    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "audio"}
            async with session.get(f"{YOUR_API_URL}/download", params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    logger.debug(f"API download request returned status {response.status}")
                else:
                    data = await response.json()
                    download_token = data.get("download_token")
                    if download_token:
                        stream_url = f"{YOUR_API_URL}/stream/{video_id}?type=audio&token={download_token}"
                        async with session.get(stream_url, timeout=aiohttp.ClientTimeout(total=300)) as file_response:
                            # handle redirect (302) or direct 200
                            if file_response.status in (301, 302):
                                redirect_url = file_response.headers.get("Location")
                                if redirect_url:
                                    async with session.get(redirect_url, timeout=aiohttp.ClientTimeout(total=300)) as final_response:
                                        if final_response.status == 200:
                                            await _write_stream_to_file(final_response.content, file_path)
                                            return file_path
                            elif file_response.status == 200:
                                await _write_stream_to_file(file_response.content, file_path)
                                return file_path
    except Exception as e:
        logger.debug(f"API download audio failed, falling back to yt-dlp: {e}")

    # fallback
    return await download_song_ytdlp(link)


async def download_video(link: str) -> Optional[str]:
    """
    يحاول أولاً تحميل الفيديو عبر الـ API (إذا متوفر)، وإلا fallback إلى yt-dlp محلي.
    يعيد مسار الملف أو None.
    """
    global YOUR_API_URL
    logger = LOGGER(__name__)

    if not YOUR_API_URL:
        await load_api_url()
        if not YOUR_API_URL:
            YOUR_API_URL = FALLBACK_API_URL

    video_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link

    if not video_id or len(video_id) < 3:
        return await download_video_ytdlp(link)

    file_path = os.path.join(DOWNLOAD_DIR, f"{video_id}.mp4")
    if os.path.exists(file_path):
        return file_path

    try:
        async with aiohttp.ClientSession() as session:
            params = {"url": video_id, "type": "video"}
            async with session.get(f"{YOUR_API_URL}/download", params=params, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    logger.debug(f"API download request returned status {response.status}")
                else:
                    data = await response.json()
                    download_token = data.get("download_token")
                    if download_token:
                        stream_url = f"{YOUR_API_URL}/stream/{video_id}?type=video&token={download_token}"
                        async with session.get(stream_url, timeout=aiohttp.ClientTimeout(total=600)) as file_response:
                            if file_response.status in (301, 302):
                                redirect_url = file_response.headers.get("Location")
                                if redirect_url:
                                    async with session.get(redirect_url, timeout=aiohttp.ClientTimeout(total=600)) as final_response:
                                        if final_response.status == 200:
                                            await _write_stream_to_file(final_response.content, file_path)
                                            return file_path
                            elif file_response.status == 200:
                                await _write_stream_to_file(file_response.content, file_path)
                                return file_path
    except Exception as e:
        logger.debug(f"API download video failed, falling back to yt-dlp: {e}")

    return await download_video_ytdlp(link)


# --- دوال المساعدة ---

async def shell_cmd(cmd: str) -> str:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        err_text = errorz.decode("utf-8", errors="ignore")
        if "unavailable videos are hidden" in err_text.lower():
            return out.decode("utf-8", errors="ignore")
        else:
            return err_text
    return out.decode("utf-8", errors="ignore")


# --- كلاس YouTubeAPI الأساسي ---

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Optional[str]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        for message in messages:
            # first check entities on text
            text = message.text or message.caption or ""
            if getattr(message, "entities", None):
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        return text[entity.offset: entity.offset + entity.length]
            # then check caption_entities for text links
            if getattr(message, "caption_entities", None):
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None) -> Optional[Tuple[str, str, int, str, str]]:
        """
        يرجع (title, duration_min, duration_sec, thumbnail, vidid) أو None لو فشل.
        """
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            res = await results.next()
            items = res.get("result")
            if not items:
                return None
            item = items[0]
            title = item.get("title", "")
            duration_min = item.get("duration", "")
            thumbnail = item.get("thumbnails", [{}])[0].get("url", "")
            vidid = item.get("id", "")
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
            return title, duration_min, duration_sec, thumbnail, vidid
        except Exception as e:
            LOGGER(__name__).error(f"VideosSearch details error: {e}")
            return None

    async def title(self, link: str, videoid: Union[bool, str] = None) -> Optional[str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            res = await results.next()
            items = res.get("result")
            if not items:
                return None
            return items[0].get("title")
        except Exception as e:
            LOGGER(__name__).error(f"VideosSearch title error: {e}")
            return None

    async def duration(self, link: str, videoid: Union[bool, str] = None) -> Optional[str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            res = await results.next()
            items = res.get("result")
            if not items:
                return None
            return items[0].get("duration")
        except Exception as e:
            LOGGER(__name__).error(f"VideosSearch duration error: {e}")
            return None

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None) -> Optional[str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            res = await results.next()
            items = res.get("result")
            if not items:
                return None
            return items[0].get("thumbnails", [{}])[0].get("url")
        except Exception as e:
            LOGGER(__name__).error(f"VideosSearch thumbnail error: {e}")
            return None

    async def video(self, link: str, videoid: Union[bool, str] = None) -> Tuple[int, Union[str, None]]:
        """
        يرجع (1, path) اذا نجح، أو (0, "خطأ الرسالة") اذا فشل.
        """
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        downloaded_file = await download_video(link)
        if downloaded_file:
            return 1, downloaded_file
        else:
            return 0, "Video download failed"

    async def playlist(self, link: str, limit: int, user_id, videoid: Union[bool, str] = None) -> list:
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        playlist = await shell_cmd(
            f"yt-dlp -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
        )
        try:
            result = [key for key in playlist.split("\n") if key]
        except Exception:
            result = []
        return result

    async def track(self, link: str, videoid: Union[bool, str] = None) -> Optional[Tuple[dict, str]]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            res = await results.next()
            items = res.get("result")
            if not items:
                return None
            item = items[0]
            title = item.get("title", "")
            duration_min = item.get("duration", "")
            vidid = item.get("id", "")
            yturl = item.get("link", "")
            thumbnail = item.get("thumbnails", [{}])[0].get("url", "")
            track_details = {
                "title": title,
                "link": yturl,
                "vidid": vidid,
                "duration_min": duration_min,
                "thumb": thumbnail,
            }
            return track_details, vidid
        except Exception as e:
            LOGGER(__name__).error(f"VideosSearch track error: {e}")
            return None

    async def formats(self, link: str, videoid: Union[bool, str] = None) -> Tuple[list, str]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        ytdl_opts = {"quiet": True}
        try:
            # yt_dlp op is blocking -> run in thread
            def _fmt_extract(l):
                with yt_dlp.YoutubeDL(ytdl_opts) as ydl:
                    return ydl.extract_info(l, download=False)

            r = await asyncio.to_thread(_fmt_extract, link)
            formats_available = []
            for fmt in r.get("formats", []):
                try:
                    if "dash" not in str(fmt.get("format", "")).lower():
                        formats_available.append(
                            {
                                "format": fmt.get("format"),
                                "filesize": fmt.get("filesize"),
                                "format_id": fmt.get("format_id"),
                                "ext": fmt.get("ext"),
                                "format_note": fmt.get("format_note"),
                                "yturl": link,
                            }
                        )
                except Exception:
                    continue
            return formats_available, link
        except Exception as e:
            LOGGER(__name__).error(f"Formats Error: {e}")
            return [], link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]:
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        try:
            a = VideosSearch(link, limit=10)
            res = await a.next()
            result = res.get("result")
            if not result or query_type >= len(result):
                return None, None, None, None
            item = result[query_type]
            title = item.get("title")
            duration_min = item.get("duration")
            vidid = item.get("id")
            thumbnail = item.get("thumbnails", [{}])[0].get("url")
            return title, duration_min, thumbnail, vidid
        except Exception as e:
            LOGGER(__name__).error(f"VideosSearch slider error: {e}")
            return None, None, None, None

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> Tuple[Optional[str], bool]:
        """
        يعيد (file_path, True) لو نجح، أو (None, False) لو فشل.
        """
        if videoid:
            link = self.base + link

        # استخدام دوال التحميل الهجينة
        if video:
            downloaded_file = await download_video(link)
        else:
            downloaded_file = await download_song(link)

        if downloaded_file:
            return downloaded_file, True
        else:
            return None, False
