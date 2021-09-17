from aiogram import types

from loader import dispatcher
from aiogram.dispatcher.filters import CommandHelp


@dispatcher.message_handler(CommandHelp())
async def help_command(message: types.Message):
    await message.answer("/check_connection — проверить соединение с сервером Active Directory; \n"
                         "/add_user_account — добавить учётную запись пользователя домена; \n"
                         "/create_user_dir — создать личную директорию пользователя и файл с паролем; \n"
                         "\n"
                         "/description_creds — описание файла <code>credentials</code> для подключения "
                         "к Active Directory; \n"                         
                         "/post_creds — передать файл <code>credentials</code> для подключения "
                         "к Active Directory; \n"
                         "\n"
                         "/help — прочитать это сообщение ещё раз. \n"
                         "\n"
                         "Если что-то идет не так и вы не понимаете, как такое возможно, "
                         "пожалуйста, напишите @arthur_dzhemakulov.")
