import asyncio
import shlex
import sys
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError

import config
from ..logging import LOGGER


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        future = asyncio.run_coroutine_threadsafe(
            install_requirements(), loop
        )
        return future.result()
    else:
        return asyncio.run(install_requirements())


def git():
    REPO_LINK = config.UPSTREAM_REPO

    if config.GIT_TOKEN:
        try:
            GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
            TEMP_REPO = REPO_LINK.split("https://")[1]
            UPSTREAM_REPO = f"https://{GIT_USERNAME}:{config.GIT_TOKEN}@{TEMP_REPO}"
        except Exception as e:
            LOGGER(__name__).error(f"خطأ في إعداد Git Token: {e}")
            UPSTREAM_REPO = config.UPSTREAM_REPO
    else:
        UPSTREAM_REPO = config.UPSTREAM_REPO

    try:
        repo = Repo(".")
        LOGGER(__name__).info("تم العثور على مستودع Git محلي")
    except InvalidGitRepositoryError:
        LOGGER(__name__).warning("لم يتم العثور على مستودع Git، جاري إنشاؤه")
        repo = Repo.init(".")

        try:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        except BaseException:
            origin = repo.remote("origin")

        origin.fetch()
        repo.create_head(
            config.UPSTREAM_BRANCH,
            origin.refs[config.UPSTREAM_BRANCH],
        )
        repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(
            origin.refs[config.UPSTREAM_BRANCH]
        )
        repo.heads[config.UPSTREAM_BRANCH].checkout(True)

    except GitCommandError as e:
        LOGGER(__name__).error(f"خطأ في Git: {e}")
        return

    try:
        origin = repo.remote("origin")
    except ValueError:
        origin = repo.create_remote("origin", UPSTREAM_REPO)

    try:
        LOGGER(__name__).info("جاري جلب التحديثات من المستودع")
        origin.fetch(config.UPSTREAM_BRANCH)
        origin.pull(config.UPSTREAM_BRANCH)
    except GitCommandError:
        LOGGER(__name__).warning("فشل pull، سيتم عمل reset إجباري")
        repo.git.reset("--hard", "FETCH_HEAD")

    LOGGER(__name__).info("جاري تثبيت المتطلبات")
    stdout, stderr, code, pid = install_req(
        f"{sys.executable} -m pip install --no-cache-dir -r requirements.txt"
    )

    if code == 0:
        LOGGER(__name__).info("تم تثبيت المتطلبات بنجاح")
    else:
        LOGGER(__name__).error(
            f"فشل تثبيت المتطلبات\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        )

    LOGGER(__name__).info("انتهت عملية التحديث بالكامل")
