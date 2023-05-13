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
    system_profile_set: bool = False
    is_reaction_positive: bool = False
    reacted_to_profiling_step: bool = False
    messages: List[Message] = None

    class Config:
        """Configs"""

        fields = {
            "id": {"include": True},
            "messages": {"include": True},
            "system_profile_set": {"include": True},
            "is_reaction_positive": {"include": True},
            "reacted_to_profiling_step": {"include": True},
        }
