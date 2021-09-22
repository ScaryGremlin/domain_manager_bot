from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from data import creds
from domain_management import misc
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from domain_management.user_account import UserAccount
from loader import dispatcher
from states import AddUserAccountQuestions


@dispatcher.message_handler(Command("add_user_account"))
async def select_fio_command(message: types.Message):
    cancel_keyboard = InlineKeyboardMarkup(row_width=1)
    cancel_button = InlineKeyboardButton(text=ResultsMessages.CANCEL,
                                         callback_data="cancel")
    cancel_keyboard.insert(cancel_button)
    await message.answer("Хорошо, сообщите мне фамилию, имя и отчество нового пользователя и его мобильный телефон.\n"
                         "Параметры передавайте через запятую!\n"
                         "Порядок параметров имеет значение!\n"
                         "Например: <code>Петушаркин Пётр Сергеевич, +7 928 077-66-55</code>",
                         reply_markup=cancel_keyboard)
    await AddUserAccountQuestions.first()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=AddUserAccountQuestions.Q1)
async def select_org_unit_button_command(message: types.Message, state: FSMContext):
    await state.update_data(answer1=message.text)
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        attrs = ["ou", "distinguishedName"]
        dm.get_all_org_units(attrs)
        misc.write_dict_in_file(f"{message.chat.id}_org_units.json", dm.get_all_org_units_as_dict())
        dm.disconnect()
        select_org_units_keyboard = InlineKeyboardMarkup(row_width=1)
        select_org_unit_button = InlineKeyboardButton(text="Выбрать подразделение",
                                                      switch_inline_query_current_chat="units")
        cancel_button = InlineKeyboardButton(text=ResultsMessages.CANCEL,
                                             callback_data="cancel")
        select_org_units_keyboard.insert(select_org_unit_button)
        select_org_units_keyboard.insert(cancel_button)
        await message.answer("Передайте название подразделения в ответном сообщении или выберите его из списка.",
                             reply_markup=select_org_units_keyboard)
        await AddUserAccountQuestions.next()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)


@dispatcher.inline_handler(text="units", state=AddUserAccountQuestions.Q2)
async def select_org_unit_command(query: types.InlineQuery):
    offset = int(query.offset) if query.offset else 0
    # Получить список подразделений из json-файла
    org_units = misc.get_dict_from_file(f"{query.from_user.id}_org_units.json")
    results = [types.InlineQueryResultArticle(
        id=org_unit[0],
        title=org_unit[0],
        input_message_content=types.InputTextMessageContent(message_text=org_unit[0]),
        description=org_unit[1]
    ) for org_unit in misc.get_slice_dict(org_units.items(), start=offset, size=50)]
    if len(results) < 50:
        # Результатов больше не будет, next_offset пустой
        await query.answer(results, is_personal=True, next_offset=None, cache_time=0)
    else:
        # Ожидаем следующую порцию данных
        await query.answer(results, is_personal=True, next_offset=str(offset + 50), cache_time=0)


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=AddUserAccountQuestions.Q2)
async def add_user_account_command(message: types.Message, state: FSMContext):
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        answer1 = await state.get_data()
        fio, mobile = misc.get_userdata_from_rawstring(answer1.get("answer1"))
        org_unit = message.text
        user_account = UserAccount(fio, org_unit, mobile)
        msg = "\n".join(dm.add_user_account(user_account)[1])
        await message.answer(msg)
        dm.disconnect()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)
    await state.finish()


@dispatcher.callback_query_handler(text="cancel", state=AddUserAccountQuestions.Q1)
async def cancel_command_q1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.finish()


@dispatcher.callback_query_handler(text="cancel", state=AddUserAccountQuestions.Q2)
async def cancel_command_q2(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.finish()
