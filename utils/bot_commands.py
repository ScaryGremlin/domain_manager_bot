from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_bot_commands(dispatcher: Dispatcher):
    await dispatcher.bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("check_connection", "Проверить соединение с сервером Active Directory"),
        BotCommand("add_user_account", "Добавить учётную запись пользователя домена"),
        BotCommand("description_settings", "Описание файла credentials для подключения к Active Directory"),
        BotCommand("post_settings", "Передать файл credentials для подключения к Active Directory"),
        BotCommand("help", "Помощь"),
    ])
