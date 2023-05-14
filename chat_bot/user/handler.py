"""
User handler class to load and save Users
"""
from pydantic import ValidationError
from chat_bot.models.user import User
from chat_bot.utils.handlers.file_handler import JsonHandler
from chat_bot.utils.handlers.path_handler import PathHandler
from chat_bot.utils.enums import Directories, Extensions
from chat_bot.utils.logger import logger


class UserHandler:
    """
    Class to load and update Chat Historial
    """

    def __init__(
        self,
        file_handler: JsonHandler = JsonHandler(),
        path_handler: PathHandler = PathHandler(),
    ) -> None:
        self.file_handler = file_handler
        self.path_handler = path_handler
        self.path_components = [
            Directories.CWD.value,
            Directories.DB.value,
            Directories.USERS.value,
        ]

    def load(self, user_id: str) -> User:
        """
        Load a User for and specific user_id

        Args:
            user_id (str): user_id

        Raises:
            v_e: File loaded don't comply with the allowed structure.

        Returns:
            User: User Model populated.
        """
        user = None
        try:
            user_path = self.path_handler.compose_path(
                [
                    *self.path_components,
                    f"{user_id}{Extensions.DOT_JSON.value}",
                ]
            )
            user = User.parse_file(user_path)
        except ValidationError as v_e:
            logger.error(v_e)
            raise v_e
        except FileNotFoundError as f_e:
            logger.warning(f_e)
        return user

    def create(self, user: User) -> bool:
        """Create a new User with her corresponding discord data.

        Args:
            user (User): Pydantic model for User.

        Raises:
            v_e: Pydantic Validation error.
            f_e: File not found.
            o_e: OS Error over directory/file operations.

        Returns:
            bool: True if the save was sucessfull, otherwise False
        """
        is_saved = False
        user_path = None
        try:
            user_path = self.path_handler.compose_path(
                [
                    *self.path_components,
                    f"{user.id}{Extensions.DOT_JSON.value}",
                ]
            )
            self.file_handler.save(user.dict(), user_path)
            is_saved = True

        except ValidationError as v_e:
            logger.error(v_e)
            raise v_e
        except FileNotFoundError as f_e:
            logger.error(f_e)
            raise f_e
        except OSError as o_e:
            logger.error(o_e)
            raise o_e
        return is_saved

    def exists(self, user_id: str) -> bool:
        """Check if an specific chat file exists.

        Args:
            user_id (str): user_id
        Returns:
            bool: True, otherwise False
        """
        chat_path = self.path_handler.compose_path([*self.path_components])
        return self.path_handler.file_exists(
            chat_path, f"{user_id}{Extensions.DOT_JSON.value}"
        )
