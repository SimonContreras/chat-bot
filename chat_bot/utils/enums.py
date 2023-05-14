"""
Enum classes
"""
import os
from enum import Enum


class Engines(Enum):
    """
    OpenAI API compatible engines
    """

    GPT_3_5_TURBO = "gpt-3.5-turbo"


class Encodings(Enum):
    """
    Encoding constants
    """

    UTF_8 = "utf-8"


class Directories(Enum):
    """
    Encoding constants
    """

    CWD = os.getcwd()
    DB = "db"
    USERS = "users"
    CHATS = "chats"


class Extensions(Enum):
    """
    Extensions constants
    """

    DOT_JSON = ".json"


class Roles(Enum):
    """
    ChatCompletion API roles available
    """

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
