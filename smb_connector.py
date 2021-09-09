import paramiko
from smb.SMBConnection import SMBConnection

import miscellaneous as misc


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
        """
        self.__smb_connection = SMBConnection(username=username,
                                              password=password,
                                              my_name="python_script",
                                              remote_name=remote_name,
                                              domain=domain,
                                              use_ntlm_v2=True)
        self.__smb_connection.connect(smb_server_ip, timeout=20)

    def create_directory(self, share: str, directory_name: str):
        self.__smb_connection.createDirectory(share, directory_name)

    def create_password_file(self, share, directory_name):
        # Создать локальную копию файла с паролем
        password = misc.get_password(password_length=8, by_chance=True)
        with open("pass.txt", "w") as pass_file:
            pass_file.write(password)

        with open("pass.txt", 'rb') as pass_file:
            uploaded_file = self.__smb_connection.storeFile(share, directory_name, "pass.txt", pass_file)

    @staticmethod
    def set_permissions(self, account_directory: str):
        with paramiko.SSHClient() as ssh_client:
            id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
            ssh_client.load_system_host_keys()
            ssh_client.connect("192.168.213.237", username="user", pkey=id_rsa)
            stdin, stdout, stderr = ssh_client.exec_command(f'c:/scripts/set_permission "{account_directory}"')
            print(stdout.read().decode("cp1252"))
        del ssh_client, stdin, stdout, stderr
