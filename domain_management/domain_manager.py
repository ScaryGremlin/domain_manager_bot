from ldap3 import Connection, Server, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException

from domain_management import misc
from domain_management.results_messages import ResultsMessages
from domain_management.user_account import UserAccount


class DomainManager:
    """
    Класс управления Active Directory
    """
    def __init__(self, server_ip: str, domain: str, login: str, password: str):
        """
        Конструктор
        :param server_ip: Адрес сервера Active Directory. DNS-имя или IP.
        :param domain: Имя домена
        :param login: NetBIOS-имя домена и логин - CO\Administrator
        :param password: Пароль
        """
        self.__ldap_server = Server(server_ip, get_info=ALL)
        self.__domain = domain
        self.__login = login
        self.__password = password
        self.__connection = self.__connect()

    def __connect(self):
        try:
            return Connection(self.__ldap_server, self.__login, self.__password, auto_bind=True)
        except LDAPException:
            return None

    @staticmethod
    def __get_search_tree(domain: str):
        return ",".join([f"DC={element}" for element in domain.split(".")])

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

    def add_user_account(self, user_account: UserAccount) -> tuple:
        """
        Добавить учётную запись пользователя
        :param user_account: Экземпляр класса учётных записей пользователей
        :return: Список ошибок или успешных выполнений команд
        """
        # Сгенерировать строку dn
        dn = self.__get_dn(user_account.surname, user_account.name, user_account.org_unit, self.__domain)
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

    def get_all_users(self, attrs: list):
        """
        Получить список всех пользователей домена
        :param attrs: Атрибуты пользователя, которые необходимо получить
        :return: Список всех пользователей домена
        """
        search_tree = self.__get_search_tree(self.__domain)
        self.__connection.search(search_tree, "(objectCategory=person)", SUBTREE, attributes=attrs)
        return self.__connection.entries

    def get_all_org_units(self):
        pass

    def disconnect(self):
        return self.__connection.unbind()

    @property
    def is_connected(self):
        return self.__connection

    @property
    def result(self):
        return self.__connection.result
