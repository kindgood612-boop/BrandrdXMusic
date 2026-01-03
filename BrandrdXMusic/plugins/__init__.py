import glob
import os
from os.path import dirname, isfile


def __list_all_modules():
    work_dir = dirname(__file__)

    # جلب كل ملفات py داخل أي فولدر فرعي
    mod_paths = glob.glob(os.path.join(work_dir, "*", "*.py"))

    all_modules = []

    for f in mod_paths:
        if not isfile(f):
            continue

        if f.endswith("__init__.py"):
            continue

        # تحويل المسار إلى اسم موديول بايثون صحيح
        module = f.replace(work_dir, "").lstrip(os.sep)
        module = module.replace(os.sep, ".")[:-3]

        all_modules.append(module)

    return all_modules


ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
