# BrandrdXMusic/core/database/users.py

from datetime import datetime
from BrandrdXMusic.core.mongo import mongodb

# =========================
# Mongo Collections
# =========================

sudoersdb = mongodb.sudoers
usersdb = mongodb.users
chatsdb = mongodb.chats
bandb = mongodb.bans
gbandb = mongodb.gbans
maintenancedb = mongodb.maintenance

# =========================
# In-Memory Cache
# =========================

sudoers = set()
users = set()
chats = set()
banned = set()
gbanned = set()
maintenance = False

# =========================
# SUDO USERS
# =========================

async def load_sudoers():
    sudoers.clear()
    async for user in sudoersdb.find({}):
        sudoers.add(user["user_id"])


async def add_sudo(user_id: int):
    sudoers.add(user_id)
    await sudoersdb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True,
    )


async def remove_sudo(user_id: int):
    sudoers.discard(user_id)
    await sudoersdb.delete_one({"user_id": user_id})


async def is_sudo(user_id: int) -> bool:
    if not sudoers:
        await load_sudoers()
    return user_id in sudoers


async def get_sudoers():
    if not sudoers:
        await load_sudoers()
    return list(sudoers)


async def get_authuser_names():
    if not sudoers:
        await load_sudoers()
    return sudoers

# =========================
# USERS
# =========================

async def add_user(user_id: int):
    if user_id in users:
        return
    users.add(user_id)
    await usersdb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id, "date": datetime.utcnow()}},
        upsert=True,
    )


async def get_users_count():
    return await usersdb.count_documents({})


# =========================
# CHATS
# =========================

async def add_chat(chat_id: int):
    if chat_id in chats:
        return
    chats.add(chat_id)
    await chatsdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"chat_id": chat_id, "date": datetime.utcnow()}},
        upsert=True,
    )


async def get_chats_count():
    return await chatsdb.count_documents({})


# =========================
# BANS (Local)
# =========================

async def ban_user(user_id: int):
    banned.add(user_id)
    await bandb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True,
    )


async def unban_user(user_id: int):
    banned.discard(user_id)
    await bandb.delete_one({"user_id": user_id})


async def is_banned(user_id: int) -> bool:
    if user_id in banned:
        return True
    data = await bandb.find_one({"user_id": user_id})
    if data:
        banned.add(user_id)
        return True
    return False


async def get_banned_users():
    return [u["user_id"] async for u in bandb.find({})]

# =========================
# GLOBAL BANS
# =========================

async def gban_user(user_id: int):
    gbanned.add(user_id)
    await gbandb.update_one(
        {"user_id": user_id},
        {"$set": {"user_id": user_id}},
        upsert=True,
    )


async def ungban_user(user_id: int):
    gbanned.discard(user_id)
    await gbandb.delete_one({"user_id": user_id})


async def is_gbanned(user_id: int) -> bool:
    if user_id in gbanned:
        return True
    data = await gbandb.find_one({"user_id": user_id})
    if data:
        gbanned.add(user_id)
        return True
    return False


async def get_gbanned_users():
    return [u["user_id"] async for u in gbandb.find({})]

# =========================
# MAINTENANCE MODE
# =========================

async def set_maintenance(status: bool):
    global maintenance
    maintenance = status
    await maintenancedb.update_one(
        {"_id": 1},
        {"$set": {"status": status}},
        upsert=True,
    )


async def get_maintenance():
    global maintenance
    if maintenance:
        return True
    data = await maintenancedb.find_one({"_id": 1})
    if not data:
        return False
    maintenance = data.get("status", False)
    return maintenance
