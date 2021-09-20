from aiogram import types
from ldap3 import ALL_ATTRIBUTES
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from data import creds
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from loader import dispatcher
from states import CreateUserDirQuestions
import json


@dispatcher.message_handler(Command("create_user_dir"))
async def select_user_button_command(message: types.Message):
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        attrs = ["sAMAccountName", "displayName", "mobile"]
        dm.get_all_users(attrs)
        with open("all_users.json", "w") as all_users_file:
            json.dump(dm.get_all_users_as_dict(), all_users_file, sort_keys=True, indent=2, ensure_ascii=False)
        dm.disconnect()
        buttons = [
            [InlineKeyboardButton(text="Выбрать пользователя", switch_inline_query_current_chat="users")]
        ]
        await message.answer("Создать директорию пользователя",
                             reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)


@dispatcher.inline_handler(text="users")
async def select_user_command(query: types.InlineQuery):
    # dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    # if dm.is_connected:
    #     query.offset = 20
    #     print(query.offset)
    #     attrs = ["sAMAccountName", "displayName", "mobile"]
    #     list_of_users = []
    #     dm.get_all_users(attrs)
    #     users_attrs_as_dict = dm.get_all_users_as_dict()
    #
    #     for i in dm.get_all_org_units(["ou"]):
    #         print(i.ou)
    #
    #     for key in sorted(users_attrs_as_dict.keys()):
    #         sm_account_name = key
    #         display_name = users_attrs_as_dict.get(key).get("Display name")
    #         mobile = users_attrs_as_dict.get(key).get("Mobile")
    #         list_of_users.append(
    #             types.InlineQueryResultArticle(
    #                 id=sm_account_name,
    #                 title=sm_account_name,
    #                 input_message_content=types.InputTextMessageContent(message_text=sm_account_name, parse_mode="HTML"),
    #                 description=f"Display name: {display_name}\nMobile: {mobile}"
    #             )
    #         )
    #     await query.answer(results=list_of_users, cache_time=0)
    #     dm.disconnect()
    # else:
    #     await query.answer(results=[
    #         types.InlineQueryResultArticle(
    #             id="0",
    #             title=ResultsMessages.ERROR_CONNECTING_AD,
    #             input_message_content=types.InputTextMessageContent(message_text=ResultsMessages.ERROR_CONNECTING_AD)
    #         )
    #     ], cache_time=0)

    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        attrs = ["sAMAccountName", "displayName", "mobile"]
        # Высчитываем offset как число
        print("query.offset =", query.offset)
        cookie = query.offset.encode("utf-8") if query.offset else None
        print("cookie =", cookie)
        cookie, all_users = dm.get_all_users(attrs, paged_size=10, paged_cookie=cookie)
        print(cookie)
        list_of_users = []
        for attr in all_users:
            list_of_users.append(types.InlineQueryResultArticle(
                id=attr["sAMAccountName"].value,
                title=attr["sAMAccountName"].value,
                input_message_content=types.InputTextMessageContent(message_text=attr["sAMAccountName"].value),
                description="description")
            )
        print("len(list_of_users) =", len(list_of_users))
        if len(list_of_users) < 10:
            # Результатов больше не будет, next_offset пустой
            await query.answer(results=list_of_users, is_personal=True, next_offset=None, cache_time=0)
        else:
            print("Ожидаем следующую пачку")
            print(cookie)
            cookie = cookie.decode("utf-8") if cookie else None
            print(cookie)
            await query.answer(results=list_of_users, is_personal=True, next_offset=cookie, cache_time=0)


def get_fake_results(start_num: int, size: int = 50):
    overall_items = 195
    # Если результатов больше нет, отправляем пустой список
    if start_num >= overall_items:
        return []
    # Отправка неполной пачки (последней)
    elif start_num + size >= overall_items:
        return list(range(start_num, overall_items+1))
    else:
        return list(range(start_num, start_num+size))
