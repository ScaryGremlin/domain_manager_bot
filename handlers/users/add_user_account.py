from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from data import creds
from domain_management.domain_manager import DomainManager
from domain_management.misc import get_userdata_from_rawstring
from loader import dispatcher
from states import AddUserAccountQuestions


@dispatcher.message_handler(Command("add_user_account"))
async def get_fio_user_account_command(message: types.Message):
    await message.answer('Хорошо, сообщите мне фамилию, имя и отчество нового пользователя, '
                         'подразделение, в которое необходимо добавить пользователя и его мобильный телефон.\n'
                         'Параметры передавайте через запятую!\n'
                         'Порядок параметров имеет значение!\n'
                         'Например: <code>Петушаркин Василий Иванович, frontoffice, +7 928 077-55-44</code>')
    await AddUserAccountQuestions.first()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=AddUserAccountQuestions.Q1)
async def add_user_account_command(message: types.Message, state: FSMContext):
    fio, org_unit, mobile = get_userdata_from_rawstring(message.text)
    dm = DomainManager(creds.AD_SERVER_IP, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        msg = "\n".join(dm.add_user_account(fio, org_unit, mobile)[1])
        await message.answer(msg)
        dm.disconnect()
        await state.finish()
