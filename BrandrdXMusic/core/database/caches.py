import asyncio

_active_audio = []
_active_video = []
_assistant_cache = {}
_count_cache = {}
_channel_connect = {}
_lang_cache = {}
_loop_state = {}
_maintenance = []
_nonadmin_cache = {}
_pause_state = {}
_playmode = {}
_playtype = {}
_skipmode = {}
_cleanmode = []
_suggestion = {}
_mute_state = {}

DB_LOCK = asyncio.Lock()
ACTIVE_LOCK = asyncio.Lock()
ASSISTANT_LOCK = asyncio.Lock()
