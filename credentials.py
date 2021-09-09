from os import getenv

from dotenv import load_dotenv

load_dotenv()

AD_SERVER_IP = getenv("AD_SERVER_IP")
AD_LOGIN = getenv("AD_LOGIN")
AD_PASSWORD = getenv("AD_PASSWORD")
DOMAIN = getenv("DOMAIN")

SMB_SERVER_IP = getenv("SMB_SERVER_IP")
SMB_SERVER_PORT = int(getenv("SMB_SERVER_PORT"))
SMB_SERVER_NAME = getenv("SMB_SERVER_NAME")
SMB_SERVER_LOGIN = getenv("SMB_SERVER_LOGIN")

RSAT_DESKTOP_IP = getenv("RSAT_DESKTOP_IP")
RSAT_DESKTOP_USERNAME = getenv("RSAT_DESKTOP_USERNAME")

SHARE = getenv("SHARE")
