"""
Env vars mapping
"""
from pydantic import BaseSettings


class DiscordSettings(BaseSettings):
    """en var mapping"""

    DISCORD_BOT_TOKEN: str


DISCORD_SETTINGS = DiscordSettings()
