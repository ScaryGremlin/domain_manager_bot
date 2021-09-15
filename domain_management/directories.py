from pathlib import Path

import paramiko

from data import creds


class Directories:
    def __init__(self, dir_name: str):
        self.__dir_name = dir_name
        self.__exists = self.__create_dir()

    def __create_dir(self):
        try:
            Path(self.__dir_name).mkdir()
        except FileExistsError:
            return False
        return True

    def set_permissions(self, login: str):
        if self.__exists:
            with paramiko.SSHClient() as ssh_client:
                id_rsa = paramiko.RSAKey.from_private_key_file("/home/member/.ssh/id_rsa")
                ssh_client.load_system_host_keys()
                ssh_client.connect(creds.AD_SERVER_IP, username=creds.SSH_USER, pkey=id_rsa)
                command = f"""smbcacls //{creds.SMB_SERVER_IP}/{creds.SHARE} {self.__dir_name} 
                    -a 'ACL:{login}:ALLOWED/OI|CI/0x001201ff' 
                    --authentication-file=/member/.creds/smbcacls_creds"""
                _, stdout, stderr = ssh_client.exec_command(command)
            return stdout, stderr
