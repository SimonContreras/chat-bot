"""
Env vars mapping
"""
from pydantic import BaseSettings


class SecretsSettings(BaseSettings):
    """en var mapping"""

    open_api_key: str
