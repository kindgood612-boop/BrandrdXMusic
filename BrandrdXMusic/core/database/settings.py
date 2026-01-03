# core/database/settings.py

from BrandrdXMusic.core.database.connections import (
    DB_LOCK,
    skipdb,
    countdb,
    autoenddb,
    channeldb,
    playtypedb,
    playmodedb,
    langdb,
    onoffdb,
    _skipmode,
    _count_cache,
    _channel_connect,
    _playtype,
    _playmode,
    _lang_cache,
    _loop_state,
    _maintenance,
)

# ==========================
# Skip Mode
# ==========================

async def is_skipmode(chat_id: int) -> bool:
    async with DB_LOCK:
        mode = _skipmode.get(chat_id)

    if mode is None:
        user = await skipdb.find_one({"chat_id": chat_id})
        val = not bool(user)
        async with DB_LOCK:
            _skipmode[chat_id] = val
        return val

    return mode


async def skip_on(chat_id: int):
    async with DB_LOCK:
        _skipmode[chat_id] = True
    await skipdb.delete_one({"chat_id": chat_id})


async def skip_off(chat_id: int):
    async with DB_LOCK:
        _skipmode[chat_id] = False
    await skipdb.insert_one({"chat_id": chat_id})


# ==========================
# Upvote Count
# ==========================

async def get_upvote_count(chat_id: int) -> int:
    async with DB_LOCK:
        mode = _count_cache.get(chat_id)

    if mode is None:
        data = await countdb.find_one({"chat_id": chat_id})
        val = data.get("mode", 5) if data else 5
        async with DB_LOCK:
            _count_cache[chat_id] = val
        return val

    return mode


async def set_upvotes(chat_id: int, mode: int):
    async with DB_LOCK:
        _count_cache[chat_id] = mode

    await countdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ==========================
# Auto End
# ==========================

async def is_autoend() -> bool:
    return bool(await autoenddb.find_one({"chat_id": 1234}))


async def autoend_on():
    await autoenddb.insert_one({"chat_id": 1234})


async def autoend_off():
    await autoenddb.delete_one({"chat_id": 1234})


# ==========================
# Loop Mode
# ==========================

async def get_loop(chat_id: int) -> int:
    async with DB_LOCK:
        return _loop_state.get(chat_id, 0)


async def set_loop(chat_id: int, mode: int):
    async with DB_LOCK:
        _loop_state[chat_id] = mode


# ==========================
# Channel Mode
# ==========================

async def get_cmode(chat_id: int):
    async with DB_LOCK:
        mode = _channel_connect.get(chat_id)

    if mode is None:
        data = await channeldb.find_one({"chat_id": chat_id})
        val = data.get("mode") if data else None
        async with DB_LOCK:
            _channel_connect[chat_id] = val
        return val

    return mode


async def set_cmode(chat_id: int, mode: int):
    async with DB_LOCK:
        _channel_connect[chat_id] = mode

    await channeldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ==========================
# Play Type / Play Mode
# ==========================

async def get_playtype(chat_id: int) -> str:
    async with DB_LOCK:
        mode = _playtype.get(chat_id)

    if mode is None:
        data = await playtypedb.find_one({"chat_id": chat_id})
        val = data.get("mode", "Everyone") if data else "Everyone"
        async with DB_LOCK:
            _playtype[chat_id] = val
        return val

    return mode


async def set_playtype(chat_id: int, mode: str):
    async with DB_LOCK:
        _playtype[chat_id] = mode

    await playtypedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


async def get_playmode(chat_id: int) -> str:
    async with DB_LOCK:
        mode = _playmode.get(chat_id)

    if mode is None:
        data = await playmodedb.find_one({"chat_id": chat_id})
        val = data.get("mode", "Direct") if data else "Direct"
        async with DB_LOCK:
            _playmode[chat_id] = val
        return val

    return mode


async def set_playmode(chat_id: int, mode: str):
    async with DB_LOCK:
        _playmode[chat_id] = mode

    await playmodedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ==========================
# Language
# ==========================

async def get_lang(chat_id: int) -> str:
    async with DB_LOCK:
        mode = _lang_cache.get(chat_id)

    if mode is None:
        data = await langdb.find_one({"chat_id": chat_id})
        val = data.get("lang", "en") if data else "en"
        async with DB_LOCK:
            _lang_cache[chat_id] = val
        return val

    return mode


async def set_lang(chat_id: int, lang: str):
    async with DB_LOCK:
        _lang_cache[chat_id] = lang

    await langdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"lang": lang}},
        upsert=True,
    )


# ==========================
# Maintenance
# ==========================

async def is_maintenance() -> bool:
    if not _maintenance:
        data = await onoffdb.find_one({"on_off": 1})
        _maintenance.append(1 if data else 2)
        return not bool(data)

    return 1 not in _maintenance


async def maintenance_on():
    _maintenance[:] = [1]
    await onoffdb.insert_one({"on_off": 1})


async def maintenance_off():
    _maintenance[:] = [2]
    await onoffdb.delete_one({"on_off": 1})
