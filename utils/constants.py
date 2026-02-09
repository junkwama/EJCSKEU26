from enum import Enum

class Regex(Enum):
    EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    PHONE = r"^\+?[1-9]\d{1,14}$"

class ProjDepth(Enum):
    SHALLOW = "shallow"
    FLAT = "flat"