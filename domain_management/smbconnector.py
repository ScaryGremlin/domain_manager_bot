import smb.smb_structs
from smb.SMBConnection import SMBConnection

from domain_management import misc


class SMBConnector:
    """
    Класс взаимодействия с smb-сервером
    """
    def __init__(self, smb_server_ip: str, username: str, password: str, domain: str, remote_name: str):
        """
        Конструктор
        :param smb_server_ip:
        :param username:
        :param password:
        :param domain:
        :param remote_name:
        """
        self.__smb_server_ip = smb_server_ip
        self.__connection = SMBConnection(username=username,
                                          password=password,
                                          my_name="python_script",
                                          remote_name=remote_name,
                                          domain=domain,
                                          use_ntlm_v2=True)

    def connect(self):
        """
        Установить соединение с smb-сервером
        :return: True, если соединение установлено успешно и False в противном случае
        """
        try:
            return self.__connection.connect(self.__smb_server_ip, timeout=10)
        except:
            return None

    def create_directory(self, share: str, directory_name: str) -> bool:
        """
        Создать директорию на smb-share
        :param share: Имя smb-share
        :param directory_name: Имя директории внутри smb-share
        :return: True, если директория создана успешно и False в противном случае
        """
        try:
            self.__connection.createDirectory(share, directory_name)
        except smb.smb_structs.OperationFailure:
            return False
        return True

    def create_password_file(self, share: str, dir_name: str, file_name: str) -> int:
        """
        Создать файл с паролем пользователя по умолчанию
        :param share: Имя smb-share
        :param dir_name: Имя директории внутри smb-share
        :param file_name: Имя файла с паролем
        :return: Количество загруженных байт в файл на smb-share
        """
        # Создать локальную копию файла с паролем
        password = misc.get_password(password_length=6, by_chance=True)
        with open(file_name, "w") as pass_file:
            pass_file.write(password)
        # Создать файл с паролем на smb-share
        with open(file_name, 'rb') as pass_file:
            return self.__connection.storeFile(share, f"{dir_name}/{file_name}", pass_file)

    def disconnect(self):
        """
        Закрыть соединене с smb-сервером
        :return:
        """
        self.__connection.close()
