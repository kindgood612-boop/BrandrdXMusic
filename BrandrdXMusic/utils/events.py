import re
from telethon import events
from BrandrdXMusic import telethn

def register(**args):
    """Registers a new message with optional prefix."""
    pattern = args.get("pattern", None)

    # تـعـريـف الـبـادئـات بـحـيـث تـكـون اخـتـيـاريـة
    # الـرمـز ? يـعـنـي أن الـعـلامـة قـد تـكـون مـوجـودة أو لا
    r_pattern = r"^[/!.]?"

    # إضـافـة خـاصـيـة تـجـاهـل حـالـة الـأحـرف (Case Insensitive)
    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if pattern:
        # اسـتـبـدال "إجـبـار الـسـلاش" بـ "الـعـلامـة الاخـتـيـاريـة"
        # إذا كـان الـبـاتـرن ^/play سـيـصـبـح ^[/!.]?play
        args["pattern"] = pattern.replace("^/", r_pattern, 1)

    def decorator(func):
        telethn.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator
