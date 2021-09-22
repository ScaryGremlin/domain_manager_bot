from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from data import creds
from domain_management import misc
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from domain_management.smbconnector import SMBConnector
from loader import dispatcher
from states import CreateUserDirQuestions


@dispatcher.message_handler(Command("create_user_dir"))
async def select_user_button_command(message: types.Message):
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        attrs = ["sAMAccountName", "displayName", "mobile"]
        dm.get_all_users(attrs)
        misc.write_dict_in_file(f"{message.chat.id}_users.json", dm.get_all_users_as_dict())
        dm.disconnect()
        select_user_keyboard = InlineKeyboardMarkup(row_width=1)
        select_user_button = InlineKeyboardButton(text="Выбрать пользователя", switch_inline_query_current_chat="users")
        cancel_button = InlineKeyboardButton(text=ResultsMessages.CANCEL,
                                             callback_data="cancel")
        select_user_keyboard.insert(select_user_button)
        select_user_keyboard.insert(cancel_button)
        await message.answer("Передайте логин пользователя в ответном сообщении или выберите его из списка.",
                             reply_markup=select_user_keyboard)
        await CreateUserDirQuestions.first()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)


@dispatcher.inline_handler(text="users", state=CreateUserDirQuestions.Q1)
async def select_user_command(query: types.InlineQuery):
    offset = int(query.offset) if query.offset else 0
    # Получить пользователей из json-файла
    all_users = misc.get_dict_from_file(f"{query.from_user.id}_users.json")
    results = [types.InlineQueryResultArticle(
        id=user_attrs[0],
        title=user_attrs[0],
        input_message_content=types.InputTextMessageContent(message_text=user_attrs[0]),
        description=f"Display name: {user_attrs[1]['Display name']}\nMobile: {user_attrs[1]['Mobile']}"
    ) for user_attrs in misc.get_slice_dict(all_users.items(), start=offset, size=50)]
    if len(results) < 50:
        # Результатов больше не будет, next_offset пустой
        await query.answer(results, is_personal=True, next_offset=None, cache_time=0)
    else:
        # Ожидаем следующую порцию данных
        await query.answer(results, is_personal=True, next_offset=str(offset + 50), cache_time=0)


@dispatcher.callback_query_handler(text="cancel", state=CreateUserDirQuestions.Q1)
async def cancel_command(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.finish()


@dispatcher.message_handler(state=CreateUserDirQuestions.Q1)
async def create_user_dir_command(message: types.Message, state: FSMContext):
    smb_connection = SMBConnector(creds.SMB_SERVER_IP,
                                  creds.SMB_SERVER_LOGIN,
                                  creds.AD_PASSWORD,
                                  creds.DOMAIN,
                                  creds.SMB_SERVER_NAME)
    if smb_connection.connect():
        if smb_connection.create_directory(creds.SHARE, message.text):
            await message.answer(ResultsMessages.DIRECTORY_AND_PASSFILE_CREATED)
        else:
            await message.answer(ResultsMessages.ERROR_CREATING_USER_DIRECTORY)
        smb_connection.disconnect()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_SMB)
    await state.finish()
