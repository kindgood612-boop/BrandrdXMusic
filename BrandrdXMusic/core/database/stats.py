from typing import Dict, Union
from .collections import queriesdb, chattopdb, userdb

async def get_queries() -> int:
    chat_id = 98324
    mode = await queriesdb.find_one({"chat_id": chat_id})
    if not mode:
        return 0
    return mode["mode"]

async def set_queries(mode: int):
    chat_id = 98324
    queries = await queriesdb.find_one({"chat_id": chat_id})
    if queries:
        mode = queries["mode"] + mode
    return await queriesdb.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )

async def get_top_chats() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        chat_id = chat["chat_id"]
        total = 0
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            if counts_ > 0:
                total += counts_
                results[chat_id] = total
    return results

async def get_global_tops() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            title_ = chat["vidid"][i]["title"]
            if counts_ > 0:
                if i not in results:
                    results[i] = {}
                    results[i]["spot"] = counts_
                    results[i]["title"] = title_
                else:
                    spot = results[i]["spot"]
                    count_ = spot + counts_
                    results[i]["spot"] = count_
    return results

async def get_particulars(chat_id: int) -> Dict[str, int]:
    ids = await chattopdb.find_one({"chat_id": chat_id})
    if not ids:
        return {}
    return ids["vidid"]

async def get_particular_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_particulars(chat_id)
    if name in ids:
        return ids[name]

async def update_particular_top(chat_id: int, name: str, vidid: dict):
    ids = await get_particulars(chat_id)
    ids[name] = vidid
    await chattopdb.update_one(
        {"chat_id": chat_id}, {"$set": {"vidid": ids}}, upsert=True
    )

async def get_userss(chat_id: int) -> Dict[str, int]:
    ids = await userdb.find_one({"chat_id": chat_id})
    if not ids:
        return {}
    return ids["vidid"]

async def get_user_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_userss(chat_id)
    if name in ids:
        return ids[name]

async def update_user_top(chat_id: int, name: str, vidid: dict):
    ids = await get_userss(chat_id)
    ids[name] = vidid
    await userdb.update_one({"chat_id": chat_id}, {"$set": {"vidid": ids}}, upsert=True)

async def get_topp_users() -> dict:
    results = {}
    async for chat in userdb.find({"chat_id": {"$gt": 0}}):
        user_id = chat["chat_id"]
        total = 0
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            if counts_ > 0:
                total += counts_
        results[user_id] = total
    return results
