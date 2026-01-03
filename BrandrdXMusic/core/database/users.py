from .collections import usersdb, blockeddb

# ===================== SERVED USERS =====================

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    return bool(user)


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    if await is_served_user(user_id):
        return
    await usersdb.insert_one({"user_id": user_id})


# ===================== BANNED USERS =====================

async def get_banned_users() -> list:
    results = []
    async for user in blockeddb.find({"user_id": {"$gt": 0}}):
        uid = user.get("user_id")
        if uid:
            results.append(uid)
    return results


async def get_banned_count() -> int:
    count = 0
    async for _ in blockeddb.find({"user_id": {"$gt": 0}}):
        count += 1
    return count


async def is_banned_user(user_id: int) -> bool:
    user = await blockeddb.find_one({"user_id": user_id})
    return bool(user)


async def add_banned_user(user_id: int):
    if await is_banned_user(user_id):
        return
    await blockeddb.insert_one({"user_id": user_id})


async def remove_banned_user(user_id: int):
    if not await is_banned_user(user_id):
        return
    await blockeddb.delete_one({"user_id": user_id})
