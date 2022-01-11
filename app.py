import os

import django
from aiogram import executor

from loader import dp
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "project.djangoadmin.djangoadmin.settings"
    )
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


if __name__ == '__main__':
    setup_django()
    import handlers
    executor.start_polling(dp, on_startup=on_startup)
