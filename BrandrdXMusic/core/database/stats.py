from typing import Dict, Union
from .collections import queriesdb, chattopdb, userdb

# ===================== QUERIES =====================

async def get_queries() -> int:
    chat_id = 98324
    data = await queriesdb.find_one({"chat_id": chat_id})
    if not data:
        return 0
    return data.get("mode", 0)


async def set_queries(mode: int):
    chat_id = 98324
    data = await queriesdb.find_one({"chat_id": chat_id})
    if data:
        mode = data.get("mode", 0) + mode
    await queriesdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"mode": mode}},
        upsert=True,
    )


# ===================== TOP CHATS =====================

async def get_top_chats() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        chat_id = chat.get("chat_id")
        vidids = chat.get("vidid", {})
        total = 0
        for i in vidids:
            counts_ = vidids[i].get("spot", 0)
            if counts_ > 0:
                total += counts_
        if total > 0:
            results[chat_id] = total
    return results


async def get_global_tops() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        vidids = chat.get("vidid", {})
        for i in vidids:
            data = vidids[i]
            counts_ = data.get("spot", 0)
            title_ = data.get("title")
            if counts_ > 0:
                if i not in results:
                    results[i] = {
                        "spot": counts_,
                        "title": title_,
                    }
                else:
                    results[i]["spot"] += counts_
    return results


# ===================== PARTICULAR CHAT =====================

async def get_particulars(chat_id: int) -> Dict[str, int]:
    data = await chattopdb.find_one({"chat_id": chat_id})
    if not data:
        return {}
    return data.get("vidid", {})


async def get_particular_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_particulars(chat_id)
    return ids.get(name, False)


async def update_particular_top(chat_id: int, name: str, vidid: dict):
    ids = await get_particulars(chat_id)
    ids[name] = vidid
    await chattopdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"vidid": ids}},
        upsert=True,
    )


# ===================== USER TOPS =====================

async def get_userss(chat_id: int) -> Dict[str, int]:
    data = await userdb.find_one({"chat_id": chat_id})
    if not data:
        return {}
    return data.get("vidid", {})


async def get_user_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_userss(chat_id)
    return ids.get(name, False)


async def update_user_top(chat_id: int, name: str, vidid: dict):
    ids = await get_userss(chat_id)
    ids[name] = vidid
    await userdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"vidid": ids}},
        upsert=True,
    )


async def get_topp_users() -> dict:
    results = {}
    async for chat in userdb.find({"chat_id": {"$gt": 0}}):
        user_id = chat.get("chat_id")
        vidids = chat.get("vidid", {})
        total = 0
        for i in vidids:
            counts_ = vidids[i].get("spot", 0)
            if counts_ > 0:
                total += counts_
        if total > 0:
            results[user_id] = total
    return results
