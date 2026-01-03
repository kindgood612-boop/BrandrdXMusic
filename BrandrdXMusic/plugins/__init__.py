import glob
import os
from os.path import dirname, isfile


def __list_all_modules():
    work_dir = dirname(__file__)
    all_modules = []

    # 1️⃣ ملفات py اللي في plugins مباشرة
    root_files = glob.glob(os.path.join(work_dir, "*.py"))

    # 2️⃣ ملفات py اللي جوه أي فولدر
    sub_files = glob.glob(os.path.join(work_dir, "*", "*.py"))

    for f in root_files + sub_files:
        if not isfile(f):
            continue

        if f.endswith("__init__.py"):
            continue

        module = f.replace(work_dir, "").lstrip(os.sep)
        module = module.replace(os.sep, ".")[:-3]

        all_modules.append(module)

    return all_modules


ALL_MODULES = sorted(set(__list_all_modules()))
__all__ = ALL_MODULES + ["ALL_MODULES"]
