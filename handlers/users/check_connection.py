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
        await message.answer(ResultsMessages.CONNECTION_TO_AD_SUCCESSFUL)
    await message.answer(ResultsMessages.ERROR_CONNECTING_AD)
