from aiogram import types
from aiogram.dispatcher.filters import Command

from data import creds
from domain_management import misc
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from loader import dispatcher


@dispatcher.message_handler(Command("get_all_users"))
async def get_all_users_command(message: types.Message):
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        attrs = ["sAMAccountName", "displayName", "mobile"]
        dm.get_all_users(attrs)
        msg = misc.pretty_print_dict(dm.get_all_users_as_dict())
        await message.answer(f"<code>{msg}</code>")
        dm.disconnect()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)
