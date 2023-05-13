"""
Env vars mapping
"""
from pydantic import BaseSettings


class OpenAISettings(BaseSettings):
    """en var mapping"""

    OPEN_API_KEY: str


OPENAI_SETTINGS = OpenAISettings()
