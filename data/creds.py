from os import getenv

from dotenv import load_dotenv

load_dotenv()

AD_SERVER_IP = getenv("AD_SERVER_IP")
SMB_SERVER_IP = getenv("SMB_SERVER_IP")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_ADMINS = getenv("BOT_ADMINS").split(",")

SSH_USER = getenv("SSH_USER")

SHARE = getenv("SHARE")


def load_creds_as_file():
    pass
