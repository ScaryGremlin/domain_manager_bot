import emoji
from ldap3 import Connection, Server, ALL

import miscellaneous as misc
from credentials import DOMAIN
from user_account import UserAccount


class DomainManager:
    """
    Класс управления Active Directory
    """

    ACCOUNT_ADDED = emoji.emojize(":check_mark: Учётная запись пользователя добавлена.\n")
    ERROR_ACCOUNT_ADDING = emoji.emojize(":cross_mark: Ошибка добавления учётной записи пользователя.\n")

    PASSWORD_SET = emoji.emojize(":check_mark: Пароль учётной записи по умолчанию установлен.\n")
    ERROR_PASSWORD_SETTING = emoji.emojize(":cross_mark: Ошибка установки пароля учётной записи.\n")

    ACCOUNT_ATTRS_CHANGED = emoji.emojize(":check_mark: Атрибуты учётной записи изменены.\n")
    ERROR_ATTRS_CHANGING = emoji.emojize(":cross_mark: Ошибка изменения арибутов учётной записи.\n")

    def __init__(self, server: str, login: str, password: str):
        """
        Конструктор
        :param server: Адрес сервера Active Directory. DNS-имя или IP.
        :param login: NetBIOS-имя домена и логин - CO\Administrator
        :param password: Пароль
        """
        ldap_server = Server(server, get_info=ALL)
        self.__connection = Connection(ldap_server, login, password, auto_bind=True)

    @staticmethod
    def __get_dn(surname: str, name: str, org_unit: str, domain: str) -> str:
        """
        Сгенерировать строку DN
        :param surname: Фамилия пользователя
        :param name: Имя пользователя
        :param org_unit: Организационная единица домена
        :param domain: Имя домена
        :return: Строка DN
        """
        cn = f"CN={name} {surname},"
        ou = f"OU={org_unit},"
        dc = ",".join([f"DC={element}" for element in domain.split(".")])
        return cn + ou + dc

    def create_user_account(self, dn: str, object_class: list, account_attrs: dict) -> bool:
        """
        Создать учётную запись пользователя
        :param dn: Строка DN
        :param object_class:
        :param account_attrs:
        :return:
        """
        return self.__connection.add(dn, object_class, account_attrs)
        # return result, self.ACCOUNT_ADDED if result else self.ERROR_ADDING_ACCOUNT

    def set_user_account_password(self, dn: str, password: str) -> tuple:
        """
        Установить пароль учётной записи пользователя
        :param dn: Строка DN
        :param password: Пароль
        :return:
        """
        result = self.__connection.extend.microsoft.modify_password(dn, password)
        return result, self.DEFAULT_PASSWORD_SET if result else self.PASSWORD_SETTING_ERROR

    def change_user_account_attrs(self, dn: str, uac_account_attrs: dict) -> tuple:
        """
        Изменить атрибуты учётной записи пользователя
        :param dn:
        :param uac_account_attrs:
        :return:
        """
        result = self.__connection.modify(dn, uac_account_attrs)
        return result, self.ACCOUNT_ATTRIBUTES_CHANGED if result else self.ERROR_CHANGING_ATTRIBUTES

    def add_user(self, fio: str, org_unit: str, mobile: str):
        """
        Добавить пользователя
        :param fio: Фамилия, имя, отчество пользователя
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя.
        :param mobile: Мобильный телефон пользователя
        :return: Список ошибок или успешных выполнений команд
        """
        result_adding_user = {
            "has_account_been_added": False,
            "has_password_been_set": False,
            "has_attrs_changed": False
        }
        user_account = UserAccount(fio, mobile)
        # Сгенерировать строку dn
        dn = self.__get_dn(user_account.surname, user_account.name, org_unit, DOMAIN)
        # Сгенерировать основные и дополнительные атрибуты учётной записи пользователя
        account_attrs, uac_account_attrs = user_account.get_account_attr()
        # object_class
        object_class = ["top", "person", "organizationalPerson", "user"]
        # Сгенерировать пароль по умолчанию - месяц и год, например, август2021
        password = misc.get_password()
        # Список возвращаемых ошибок или успешных выполнений команд
        return_codes = []
        error = True

        if not self.__connection.add(dn, object_class, account_attrs):
            return result_adding_user
        elif not self.__connection.extend.microsoft.modify_password(dn, password):
            result_adding_user.update({"has_account_been_added": True})
            return result_adding_user
        elif not self.__connection.modify(dn, uac_account_attrs):
            result_adding_user.update({"has_password_been_set": True})
            return result_adding_user
        result_adding_user.update({"has_attrs_changed": True})
        return result_adding_user

        # if self.__connection.add(dn, object_class, account_attrs):
        #     # Учётная запись пользователя добавлена
        #     return_codes.append(self.ACCOUNT_ADDED)
        #     if self.__connection.extend.microsoft.modify_password(dn, password):
        #         # Пароль учётной записи по умолчанию установлен
        #         return_codes.append(self.DEFAULT_PASSWORD_SET)
        #         if self.__connection.modify(dn, uac_account_attrs):
        #             # Атрибуты учётной записи изменены
        #             return_codes.append(self.ACCOUNT_ATTRIBUTES_CHANGED)
        #             error = False
        #         else:
        #             # Ошибка изменения арибутов учётной записи
        #             return_codes.append(self.ERROR_CHANGING_ATTRIBUTES)
        #     else:
        #         # Ошибка установки пароля учётной записи
        #         return_codes.append(self.PASSWORD_SETTING_ERROR)
        # else:
        #     # Ошибка добавления учётной записи пользователя
        #     return_codes.append(self.ERROR_ADDING_ACCOUNT)

        # self.__connection.unbind()
        # # Вернуть True, если была ошибка, иначе - False и список с пояснениями выполнения операций
        # return error, return_codes
