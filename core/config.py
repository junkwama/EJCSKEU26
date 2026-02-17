from enum import Enum

class Config(Enum): 
    DEFAULT_ITEMS_PER_PAGE = 10
    PREVIEW_LIST_ITEM_NUMBER = 5
    MAX_ITEMS_PER_PAGE = 100
    SIGNED_URL_EXPIRATION_PUBLIC_FILE=(24 * 7) * 60 * 60, # secs = 24 * 7 hours = 7 day
    SIGNED_URL_EXPIRATION_PRIVATE_FILE=30 * 60, # 30 mins