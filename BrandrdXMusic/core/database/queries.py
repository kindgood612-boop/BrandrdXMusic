from .collections import queriesdb

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
        upsert=True
    )
