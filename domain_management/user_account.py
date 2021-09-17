from ldap3 import MODIFY_REPLACE


class UserAccount:
    """
    Класс учётных записей пользователей
    """
    def __init__(self, fio: str, org_unit: str, mobile: str):
        """
        Конструктор
        :param fio: Фамилия, имя и отчетсво пользователя
        """
        self.__surname, self.__name, self.__middle_name, self.__login = self.__requisites_to_data(fio)
        self.__org_unit = org_unit
        self.__mobile = mobile

    @staticmethod
    def __requisites_to_data(fio) -> tuple:
        """
        Преобразовать фамилию, имя и отчество в данные.
        Данные - фамилия, имя, отчество и имя директории упакованны в кортеж.
        Имя директории в формате Фамилия_ИО.
        :param fio: Фамилия, имя и отчество
        :return: Имя директории
        """
        surname, name, middle_name = [element.strip().capitalize() for element in fio.split()]
        login = f"{surname}_{name[0]}{middle_name[0]}"
        return surname, name, middle_name, login

    def get_account_attr(self) -> tuple:
        """
        Получить атрибуты учётной записи пользователя
        :return: Кортеж основных и дополнительных атрибутов
        """
        # Установить основные атрибуты учётной записи.
        # Фамилия, имя, логин для входа - Фамилия_ИО, отображаемое имя и мобильный телефон.
        account_attrs = {
            "sn": self.__surname,
            "givenName": self.__name,
            "sAMAccountName": self.__login,
            "displayName": f"{self.__name} {self.__surname}",
            "mobile": self.__mobile
        }
        # Установить дополнителные атрибуты учётной записи.
        # userAccountControl: 512 - включенная учётная запись,
        # pwdLastSet: 0 - требовать смену пароля при первом входе.
        uac_account_attrs = {
            "userAccountControl": (MODIFY_REPLACE, [512]),
            "pwdLastSet": (MODIFY_REPLACE, [0])
        }
        return account_attrs, uac_account_attrs

    @property
    def surname(self):
        return self.__surname

    @property
    def name(self):
        return self.__name

    @property
    def middle_name(self):
        return self.__middle_name

    @property
    def login(self):
        return self.__login

    @property
    def personal_dir(self):
        return self.__login

    @property
    def org_unit(self):
        return self.__org_unit

    @property
    def mobile(self):
        return self.__mobile
