import os
from config import autoclean


async def auto_clean(popped):
    if not popped:
        return

    rem = popped.get("file")
    if not rem:
        return

    # إزالة الملف من قائمة autoclean إن وجد
    try:
        if rem in autoclean:
            autoclean.remove(rem)
    except:
        pass

    # لو لسه مستخدم في طابور تاني
    if autoclean.count(rem) > 0:
        return

    # عدم حذف الملفات الافتراضية أو الرمزية
    if (
        rem.startswith("vid_")
        or rem.startswith("live_")
        or rem.startswith("index_")
    ):
        return

    # حذف الملف فعليًا
    try:
        if os.path.isfile(rem):
            os.remove(rem)
    except:
        pass
