"""
User model
"""

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class User(BaseModel):
    """
    User model
    """

    id: int
    name: str
    display_name: str
    discriminator: str
