"""
Message model for OpenAI API calls
"""
from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from chat_bot.utils.enums import Roles


class Message(BaseModel):
    """
    Message model
    """

    role: Roles
    content: str
    name: Optional[str] = None

    class Config:
        """Configs"""

        use_enum_values = True
        fields = {
            "role": {"include": True},
            "content": {"include": True},
            "name": {"include": True},
        }
