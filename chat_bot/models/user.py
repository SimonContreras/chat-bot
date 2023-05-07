"""
User model
"""

from pydantic import BaseModel, EmailStr  # pylint: disable=no-name-in-module


class User(BaseModel):
    """
    User model
    """

    id: str
    username: str
    name: str
    email: EmailStr
