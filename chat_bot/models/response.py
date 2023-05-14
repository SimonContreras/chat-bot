"""
Response model for OpenAI API calls
"""
from typing import List

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from chat_bot.models.message import Message


class Choice(BaseModel):
    """
    Internal model for OpenAI API response for ChatCompletion
    """

    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    """
    Internal model for OpenAI API response for ChatCompletion
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    """
    Main model for OpenAI API response for ChatCompletion
    """

    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage
