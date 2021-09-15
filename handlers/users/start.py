from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dispatcher


@dispatcher.message_handler(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Бот готов принимать команды!")
