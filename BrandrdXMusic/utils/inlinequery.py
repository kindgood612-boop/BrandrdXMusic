from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

answer = []

answer.extend(
    [
        InlineQueryResultArticle(
            title="『 إيـقـاف مـؤقـت 』",
            description="« لإيـقـاف الـتـشـغـيـل مـؤقـتـاً فـي الـمـكـالـمـة »",
            thumb_url="https://files.catbox.moe/exvq3d.jpg",
            input_message_content=InputTextMessageContent("pause"),
        ),
        InlineQueryResultArticle(
            title="『 إسـتـكـمـال 』",
            description="« لإسـتـكـمـال تـشـغـيـل الـأغـنـيـة الـمـتـوقـفـة »",
            thumb_url="https://files.catbox.moe/kmn0a6.jpg",
            input_message_content=InputTextMessageContent("resume"),
        ),
        InlineQueryResultArticle(
            title="『 تـخـطـي 』",
            description="« لـتـخـطـي الـأغـنـيـة الـحـالـيـة والـتـالـيـة »",
            thumb_url="https://files.catbox.moe/zs9g3f.jpg",
            input_message_content=InputTextMessageContent("skip"),
        ),
        InlineQueryResultArticle(
            title="『 إنـهـاء 』",
            description="« لإنـهـاء الـتـشـغـيـل ومـغـادرة الـمـسـاعـد »",
            thumb_url="https://files.catbox.moe/b91yyd.jpg",
            input_message_content=InputTextMessageContent("end"),
        ),
        InlineQueryResultArticle(
            title="『 خـلـط 』",
            description="« لـخـلـط قـائـمـة الـانـتـظـار عـشـوائـيـاً »",
            thumb_url="https://files.catbox.moe/wqipfn.jpg",
            input_message_content=InputTextMessageContent("shuffle"),
        ),
        InlineQueryResultArticle(
            title="『 تـكـرار 』",
            description="« لـتـكـرار الـأغـنـيـة الـحـالـيـة »",
            thumb_url="https://files.catbox.moe/4qhfqw.jpg",
            input_message_content=InputTextMessageContent("loop 3"),
        ),
    ]
)
