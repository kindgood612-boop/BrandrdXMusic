from .collections import (
    skipmode, skipdb, count, countdb, autoend, autoenddb,
    loop, channelconnect, channeldb, playtype, playtypedb,
    playmode, playmodedb, langm, langdb, pause, mute,
    suggestion, suggdb, cleanmode, cleandb
)

# ===================== SKIP MODE =====================

async def is_skipmode(chat_id: int) -> bool:
    mode = skipmode.get(chat_id)
    if mode is None:
        user = await skipdb.find_one({"chat_id": chat_id})
        if not user:
            skipmode[chat_id] = True
            return True
        skipmode[chat_id] = False
        return False
    return mode


async def skip_on(chat_id: int):
    skipmode[chat_id] = True
    user = await skipdb.find_one({"chat_id": chat_id})
    if user:
        await skipdb.delete_one({"chat_id": chat_id})


async def skip_off(chat_id: int):
    skipmode[chat_id] = False
    user = await skipdb.find_one({"chat_id": chat_id})
    if not user:
        await skipdb.insert_one({"chat_id": chat_id})


# ===================== UPVOTES =====================

async def get_upvote_count(chat_id: int) -> int:
    mode = count.get(chat_id)
    if mode is None:
        data = await countdb.find_one({"chat_id": chat_id})
        if not data:
            return 5
        count[chat_id] = data["mode"]
        return data["mode"]
    return mode


async def set_upvotes(chat_id: int, mode: int):
    count[chat_id] = mode
    await countdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ===================== AUTO END =====================

async def is_autoend() -> bool:
    chat_id = 1234  # Global flag (متوافق مع السورس)
    return bool(await autoenddb.find_one({"chat_id": chat_id}))


async def autoend_on():
    chat_id = 1234
    await autoenddb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id}},
        upsert=True,
    )


async def autoend_off():
    chat_id = 1234
    await autoenddb.delete_one({"chat_id": chat_id})


# ===================== LOOP =====================

async def get_loop(chat_id: int) -> int:
    return loop.get(chat_id, 0)


async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode


# ===================== CHANNEL MODE =====================

async def get_cmode(chat_id: int):
    mode = channelconnect.get(chat_id)
    if mode is None:
        data = await channeldb.find_one({"chat_id": chat_id})
        if not data:
            return None
        channelconnect[chat_id] = data["mode"]
        return data["mode"]
    return mode


async def set_cmode(chat_id: int, mode: int):
    channelconnect[chat_id] = mode
    await channeldb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ===================== PLAY TYPE =====================

async def get_playtype(chat_id: int) -> str:
    mode = playtype.get(chat_id)
    if mode is None:
        data = await playtypedb.find_one({"chat_id": chat_id})
        if not data:
            playtype[chat_id] = "Everyone"
            return "Everyone"
        playtype[chat_id] = data["mode"]
        return data["mode"]
    return mode


async def set_playtype(chat_id: int, mode: str):
    playtype[chat_id] = mode
    await playtypedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ===================== PLAY MODE =====================

async def get_playmode(chat_id: int) -> str:
    mode = playmode.get(chat_id)
    if mode is None:
        data = await playmodedb.find_one({"chat_id": chat_id})
        if not data:
            playmode[chat_id] = "Direct"
            return "Direct"
        playmode[chat_id] = data["mode"]
        return data["mode"]
    return mode


async def set_playmode(chat_id: int, mode: str):
    playmode[chat_id] = mode
    await playmodedb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ===================== LANGUAGE =====================

async def get_lang(chat_id: int) -> str:
    lang = langm.get(chat_id)
    if lang is None:
        data = await langdb.find_one({"chat_id": chat_id})
        if not data:
            langm[chat_id] = "en"
            return "en"
        langm[chat_id] = data["lang"]
        return data["lang"]
    return lang


async def set_lang(chat_id: int, lang: str):
    langm[chat_id] = lang
    await langdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"lang": lang}},
        upsert=True,
    )


# ===================== MUSIC STATE =====================

async def is_music_playing(chat_id: int) -> bool:
    return pause.get(chat_id, False)


async def music_on(chat_id: int):
    pause[chat_id] = True


async def music_off(chat_id: int):
    pause[chat_id] = False


# ===================== MUTE =====================

async def is_muted(chat_id: int) -> bool:
    return mute.get(chat_id, False)


async def mute_on(chat_id: int):
    mute[chat_id] = True


async def mute_off(chat_id: int):
    mute[chat_id] = False


# ===================== SUGGESTION =====================

async def is_suggestion(chat_id: int) -> bool:
    mode = suggestion.get(chat_id)
    if mode is None:
        user = await suggdb.find_one({"chat_id": chat_id})
        if not user:
            suggestion[chat_id] = True
            return True
        suggestion[chat_id] = False
        return False
    return mode


async def suggestion_on(chat_id: int):
    suggestion[chat_id] = True
    user = await suggdb.find_one({"chat_id": chat_id})
    if user:
        await suggdb.delete_one({"chat_id": chat_id})


async def suggestion_off(chat_id: int):
    suggestion[chat_id] = False
    user = await suggdb.find_one({"chat_id": chat_id})
    if not user:
        await suggdb.insert_one({"chat_id": chat_id})


# ===================== CLEAN MODE =====================

async def is_cleanmode_on(chat_id: int) -> bool:
    return chat_id not in cleanmode


async def cleanmode_off(chat_id: int):
    if chat_id not in cleanmode:
        cleanmode.append(chat_id)


async def cleanmode_on(chat_id: int):
    try:
        cleanmode.remove(chat_id)
    except ValueError:
        pass
