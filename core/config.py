from enum import Enum

class Config(Enum): 
    ALLOWED_HOSTS = ["*"]
    DEBUG = True
    DEFAULT_ITEMS_PER_PAGE = 10
    MAX_ITEMS_PER_PAGE = 100
    SIGNED_URL_EXPIRATION_PUBLIC_FILE = (24 * 7) * 60 * 60  # secs = 24 * 7 hours = 7 day
    SIGNED_URL_EXPIRATION_PRIVATE_FILE = 30 * 60  # 30 mins
