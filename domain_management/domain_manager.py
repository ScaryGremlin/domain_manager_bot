from ldap3 import Connection, Server, ALL
from ldap3.core.exceptions import LDAPException

from data.creds import DOMAIN
from domain_management import misc
from domain_management.results_messages import ResultsMessages
from domain_management.user_account import UserAccount


class DomainManager:
    """
    Класс управления Active Directory
    """
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

    def add_user_account(self, fio: str, org_unit: str, mobile: str) -> tuple:
        """
        Добавить пользователя
        :param fio: Фамилия, имя, отчество пользователя
        :param org_unit: Организационная еденица домена. Подразделение, в которое добавить пользователя.
        :param mobile: Мобильный телефон пользователя
        :return: Список ошибок или успешных выполнений команд
        """
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
            return (False, (ResultsMessages.ERROR_USER_ACCOUNT_ADDING,
                            ResultsMessages.ERROR_USER_PASSWORD_SETTING,
                            ResultsMessages.ERROR_USER_ACCOUNTS_ATTRS_CHANGING))
        elif not self.__connection.extend.microsoft.modify_password(dn, password):
            return (False, (ResultsMessages.USER_ACCOUNT_ADDED,
                            ResultsMessages.ERROR_USER_PASSWORD_SETTING,
                            ResultsMessages.ERROR_USER_ACCOUNTS_ATTRS_CHANGING))
        elif not self.__connection.modify(dn, uac_account_attrs):
            return (False, (ResultsMessages.USER_ACCOUNT_ADDED,
                            ResultsMessages.USER_PASSWORD_SET,
                            ResultsMessages.ERROR_USER_ACCOUNTS_ATTRS_CHANGING))
        return (True, (ResultsMessages.USER_ACCOUNT_ADDED,
                       ResultsMessages.USER_ACCOUNT_ATTRS_CHANGED,
                       ResultsMessages.USER_PASSWORD_SET))

    def disconnect(self):
        return self.__connection.unbind()

    @property
    def is_connected(self):
        return self.__connection

    @property
    def result(self):
        return self.__connection.result
