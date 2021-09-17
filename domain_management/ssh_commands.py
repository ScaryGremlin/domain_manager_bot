class SSHCommands:
    """
    Класс ssh-команд
    """
    cmd_set_acl_on_dir = "sudo smbcacls //{}/{} {} " \
                         "-a 'ACL:{}:ALLOWED/OI|CI/0x001201ff' " \
                         "--authentication-file=/home/member/.creds/smbcacls_creds"
    cmd_set_acl_on_passfile = ""
