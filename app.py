from aiogram import Dispatcher
from aiogram import executor

from loader import dispatcher
import handlers
from utils.notify_admins import on_startup_notify
from utils.bot_commands import set_bot_commands


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    await on_startup_notify(dp)


if __name__ == "__main__":
    executor.start_polling(dispatcher, on_startup=on_startup)
