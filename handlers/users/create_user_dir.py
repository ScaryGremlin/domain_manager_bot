from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from data import creds
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from loader import dispatcher
from states import CreateUserDirQuestions


@dispatcher.message_handler(Command("create_user_dir"))
async def select_user_button_command(message: types.Message):
    buttons = [
        [InlineKeyboardButton(text="Выбрать пользователя", switch_inline_query_current_chat="users")]
    ]
    await message.answer("Создать директорию пользователя", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    await CreateUserDirQuestions.first()


@dispatcher.inline_handler(text="users", state=CreateUserDirQuestions.Q1)
async def select_user_command(query: types.InlineQuery, state: FSMContext):
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        attrs = ["sAMAccountName", "displayName", "mobile"]
        list_of_users = []
        dict_of_users = {}
        for user in dm.get_all_users(attrs):
            dict_of_users.update({str(user.sAMAccountName): [str(user.displayName), str(user.mobile)]})
        for key in sorted(dict_of_users.keys()):
            sm_account_name = key
            display_name, mobile = dict_of_users.get(key)
            list_of_users.append(
                types.InlineQueryResultArticle(
                    id=str(sm_account_name),
                    title=str(sm_account_name),
                    input_message_content=types.InputTextMessageContent(message_text=sm_account_name),
                    description=f"Display name: {display_name}\nMobile: {mobile}"
                )
            )
        await query.answer(results=list_of_users)
    else:
        await query.answer(results=[
            types.InlineQueryResultArticle(
                id="0",
                title=ResultsMessages.ERROR_CONNECTING_AD,
                input_message_content=types.InputTextMessageContent(message_text=ResultsMessages.ERROR_CONNECTING_AD)
            )
        ])
