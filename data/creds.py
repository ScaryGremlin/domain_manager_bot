from os import getenv

from dotenv import load_dotenv

load_dotenv()

AD_SERVER_IP = getenv("AD_SERVER_IP")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_ADMINS = getenv("BOT_ADMINS").split(",")


def load_creds_as_file():
    pass
