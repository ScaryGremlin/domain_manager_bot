from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import creds

bot = Bot(token=creds.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
