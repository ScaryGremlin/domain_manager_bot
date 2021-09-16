from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_ADMINS = getenv("BOT_ADMINS").split(",")

AD_SERVER_IP = getenv("AD_SERVER_IP")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")

SMB_SERVER_IP = getenv("SMB_SERVER_IP")
SMB_SERVER_NAME = getenv("SMB_SERVER_NAME")
SMB_SERVER_LOGIN = getenv("SMB_SERVER_LOGIN")

SSH_SERVER_IP = getenv("SSH_SERVER_IP")
SSH_USER = getenv("SSH_USER")
SSH_SUDO_PASSWORD = getenv("SSH_SUDO_PASSWORD")

SHARE = getenv("SHARE")


def load_creds_as_file():
    pass
