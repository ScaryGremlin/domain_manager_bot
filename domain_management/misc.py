import random
from datetime import datetime

import paramiko


def get_password(password_length=6, by_chance=None) -> str:
    """
    Сгенерировать пароль пользователя по умолчанию.
    Если by_chance=True, то пароль - набор случайных символов, длинной password_length.
    Если by_chance=None, то пароль - текщий месяц, плюс год со строчной буквы, например, май2021.
    :return: Пароль пользователя
    """
    if by_chance:
        numbers = "1234567890"
        letters_lower = "abcdefghijklmnopqrstuvwxyz"
        letters_upper = letters_lower.upper()
        sequence = list(numbers + letters_lower + letters_upper)
        # Перемешать список
        random.shuffle(sequence)
        return "".join([random.choice(sequence) for _ in range(password_length)])
    else:
        list_of_months = ["январь", "февраль", "март", "апрель", "май", "июнь",
                          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
        date = datetime.now()
        month = date.month
        year = date.year
        return list_of_months[month - 1] + str(year)


def get_userdata_from_rawstring(raw_string: str) -> list:
    """
    Получить данные пользователя - ФИО, подразделение, мобильный телефон в виде списка
    Строка, разделяется по запятой в список, с удалением символов пробела в начале и в конце каждого элемента списка
    :param raw_string: Сырая строка данных
    :return: Список данных
    """
    return [element.strip() for element in raw_string.split(",")]


def execute_ssh_command_as_sudo(server_ip: str, username: str, sudo_password: str, command: str) -> tuple:
    """
    Выполнить команду по ssh
    :param server_ip: ip-адрес ssh-сервера
    :param username: Имя пользователя для подключения к ssh-серверу
    :param sudo_password: Пароль пользователя с правами sudo
    :param command: Команда, которую необходимо выполнить по ssh
    :return: Поток вывода и поток ошибок выполнения команды ssh
    """
    with paramiko.SSHClient() as ssh_client:
        id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
        ssh_client.load_system_host_keys()
        print(server_ip)
        print(username)

        ssh_client.connect("192.168.213.235", username="member", pkey=id_rsa)
        # ssh_client.connect(server_ip, username=username, pkey=id_rsa)
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        command_c = "sudo smbcacls //192.168.213.238/exchange 123 -a 'ACL:Джемакулов_АА:ALLOWED/OI|CI/0x001201ff' --authentication-file=/home/member/.creds/smbcacls_creds"
        command_b = "sudo ls -la"
        # stdin, stdout, stderr = ssh_client.exec_command(command_c, get_pty=True)
        stdin.write(f"{sudo_password}\n")
        stdin.flush()
        print(stdout.readlines())
    return stdout, stderr
