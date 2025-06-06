from enum import Enum


class Role(str, Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
