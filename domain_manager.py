import emoji
from ldap3 import Connection, Server, ALL
from ldap3.core.exceptions import LDAPException

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

    def __init__(self, server_ip: str, login: str, password: str):
        """
        Конструктор
        :param server: Адрес сервера Active Directory. DNS-имя или IP.
        :param login: NetBIOS-имя домена и логин - CO\Administrator
        :param password: Пароль
        """
        self.__ldap_server = Server(server_ip, get_info=ALL)
        self.__login = login
        self.__password = password
        self.__connection = self.__connect()

    def __connect(self):
        try:
            return Connection(self.__ldap_server, self.__login, self.__password, auto_bind=True)
        except LDAPException:
            return None

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

    def add_user_account(self, fio: str, org_unit: str, mobile: str):
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

    @property
    def is_connected(self):
        return self.__connection
