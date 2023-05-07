"""
Chat Historial model
"""

from typing import List

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from chat_bot.models.message import Message


class ChatHistorial(BaseModel):
    """
    Main model to store Chat Historial data.
    """

    id: str
    messages: List[Message]

    class Config:
        """Configs"""

        fields = {"id": {"include": True}, "messages": {"include": True}}
