import random
from typing import Optional

from BrandrdXMusic import userbot
from .collections import assdb, assistantdict


# ======================
# Basic Helpers
# ======================

async def get_assistant_number(chat_id: int) -> Optional[int]:
    return assistantdict.get(chat_id)


async def get_client(assistant: int):
    assistant = int(assistant)
    if assistant == 1:
        return userbot.one
    elif assistant == 2:
        return userbot.two
    elif assistant == 3:
        return userbot.three
    elif assistant == 4:
        return userbot.four
    elif assistant == 5:
        return userbot.five
    return None


# ======================
# Database Setters
# ======================

async def set_assistant_new(chat_id: int, number: int):
    number = int(number)
    assistantdict[chat_id] = number
    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": number}},
        upsert=True,
    )


async def set_assistant(chat_id: int):
    from BrandrdXMusic.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant

    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )

    return await get_client(ran_assistant)


# ======================
# Get Assistant (Userbot)
# ======================

async def get_assistant(chat_id: int):
    from BrandrdXMusic.core.userbot import assistants

    assistant = assistantdict.get(chat_id)

    if not assistant:
        dbassistant = await assdb.find_one({"chat_id": chat_id})

        if not dbassistant:
            return await set_assistant(chat_id)

        got_assis = int(dbassistant.get("assistant", 0))
        if got_assis in assistants:
            assistantdict[chat_id] = got_assis
            return await get_client(got_assis)

        return await set_assistant(chat_id)

    if assistant in assistants:
        return await get_client(assistant)

    return await set_assistant(chat_id)


# ======================
# Calls Assistant Logic
# ======================

async def set_calls_assistant(chat_id: int) -> int:
    from BrandrdXMusic.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistantdict[chat_id] = ran_assistant

    await assdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )

    return ran_assistant


async def group_assistant(self, chat_id: int):
    """
    IMPORTANT:
    This function MUST return a PyTgCalls instance
    (self.one / self.two / ...)
    """
    from BrandrdXMusic.core.userbot import assistants

    assistant = assistantdict.get(chat_id)

    if not assistant:
        dbassistant = await assdb.find_one({"chat_id": chat_id})

        if not dbassistant:
            assis = await set_calls_assistant(chat_id)
        else:
            assis = int(dbassistant.get("assistant", 0))
            if assis in assistants:
                assistantdict[chat_id] = assis
            else:
                assis = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)

    assis = int(assis)

    if assis == 1:
        return self.one
    elif assis == 2:
        return self.two
    elif assis == 3:
        return self.three
    elif assis == 4:
        return self.four
    elif assis == 5:
        return self.five

    # Fallback (safety)
    return self.one
