from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from data import creds
from domain_management import misc
from domain_management.domain_manager import DomainManager
from domain_management.results_messages import ResultsMessages
from domain_management.user_account import UserAccount
from loader import dispatcher
from states import AddUserAccountQuestions


@dispatcher.message_handler(Command("add_user_account"))
async def get_fio_user_account_command(message: types.Message):
    await message.answer('Хорошо, сообщите мне фамилию, имя и отчество нового пользователя, '
                         'подразделение, в которое необходимо добавить пользователя и его мобильный телефон.\n'
                         'Параметры передавайте через запятую!\n'
                         'Порядок параметров имеет значение!\n'
                         'Например: <code>Петушаркин Пётр Сергеевич, frontoffice, +7 928 077-55-44</code>')
    await AddUserAccountQuestions.first()


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=AddUserAccountQuestions.Q1)
async def add_user_account_command(message: types.Message, state: FSMContext):
    dm = DomainManager(creds.AD_SERVER_IP, creds.DOMAIN, creds.AD_LOGIN, creds.AD_PASSWORD)
    if dm.is_connected:
        fio, org_unit, mobile = misc.get_userdata_from_rawstring(message.text)
        user_account = UserAccount(fio, org_unit, mobile)
        msg = "\n".join(dm.add_user_account(user_account)[1])
        await message.answer(msg)
        dm.disconnect()
        await state.finish()
    else:
        await message.answer(ResultsMessages.ERROR_CONNECTING_AD)
