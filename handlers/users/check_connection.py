from aiogram import types
from aiogram.dispatcher.filters import Command

from data import creds
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from loader import dispatcher


@dispatcher.message_handler(Command("check_connection"))
async def check_connection_command(message: types.Message):
    dm = DomainManager(creds.AD_SERVER_IP, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        code_connect = f"<code>{dm.result}</code>"
        msg_result = f"{ResultsMessages.CONNECTION_TO_AD_SUCCESSFUL}\n{code_connect}"
        await message.answer(msg_result)
        dm.disconnect()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)
