from BrandrdXMusic.core.misc import db

async def set_queries(count: int):
    try:
        db["queries"] = count
    except Exception:
        pass
