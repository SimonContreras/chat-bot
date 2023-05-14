"""
Env vars mapping
"""
from pydantic import BaseSettings


class OpenAISettings(BaseSettings):
    """en var mapping"""

    OPENAI_API_KEY: str


OPENAI_SETTINGS = OpenAISettings()
