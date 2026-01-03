import os
from ..logging import LOGGER


def dirr():
    """
    هذه الدالة مسؤولة عن:
    1- تنظيف الصور المؤقتة من مجلد التشغيل
    2- إنشاء المجلدات الأساسية المطلوبة لتشغيل البوت
    """

    # الامتدادات التي سيتم حذفها
    image_extensions = (".jpg", ".jpeg", ".png")

    # مجلد التشغيل الحالي
    base_dir = os.getcwd()

    # حذف الصور المؤقتة من مجلد التشغيل
    for file in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file)

        if file.lower().endswith(image_extensions) and os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                LOGGER(__name__).warning(
                    f"تعذر حذف الملف المؤقت {file}: {e}"
                )

    # إنشاء المجلدات الضرورية إذا لم تكن موجودة
    try:
        os.makedirs("downloads", exist_ok=True)
        os.makedirs("cache", exist_ok=True)
    except Exception as e:
        LOGGER(__name__).error(
            f"حدث خطأ أثناء إنشاء المجلدات الأساسية: {e}"
        )
        return

    LOGGER(__name__).info("تم تحديث المجلدات وتنظيف الملفات المؤقتة بنجاح")
