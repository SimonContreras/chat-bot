"""
History handler class to load and save chat historial
"""
from pathlib import Path
from pydantic import ValidationError
from chat_bot.models.historial import ChatHistorial
from chat_bot.models.message import Message
from chat_bot.utils.handlers.file_handler import JsonHandler
from chat_bot.utils.handlers.path_handler import PathHandler
from chat_bot.utils.enums import Directories, Extensions
from chat_bot.utils.logger import logger


class ChatHistorialHandler:
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
            Directories.CHATS.value,
        ]

    def load(self, user_id: str, chat_id: str) -> ChatHistorial:
        """
        Load an historial chat for an specific user

        Args:
            user_id (str): user_id
            chat_id (str): chat_id related to the user_id

        Raises:
            v_e: File loaded don't comply with the allowed structure.

        Returns:
            ChatHistorial: ChatHistorial Model populated.
        """
        chat_historial = None
        try:
            historial_user_chat_path = self.path_handler.compose_path(
                [
                    *self.path_components,
                    user_id,
                    f"{chat_id}{Extensions.DOT_JSON.value}",
                ]
            )
            chat_historial = ChatHistorial.parse_file(historial_user_chat_path)
        except ValidationError as v_e:
            logger.error(v_e)
            raise v_e
        except FileNotFoundError as f_e:
            logger.warning(f_e)
        return chat_historial

    def update(
        self,
        user_id: str,
        chat_id: str,
        new_prompt: Message = None,
        new_response: Message = None,
        reacted_to_profiling_step: bool = False,
        is_reaction_positive: bool = False,
        system_profile_set: bool = False,
    ) -> bool:
        """Update existing ChatHistorial with a new prompt  and or update flags

        Args:
            user_id (str): user id.
            chat_id (str): chat id.
            new_prompt (Message): New prompt to be saved.
            new_response (Message): New response to be saved.
            reacted_to_profiling_step (bool): Flag to be updated.
             is_reaction_positive (bool): Flag to be updated.
            system_profile_set (bool): Flag to be updated.

        Raises:
            v_e: Pydantic Validation error.
            f_e: File not found.
            o_e: OS Error over directory/file operations.

        Returns:
            bool: True if the update was sucessfull, otherwise False
        """
        is_saved = False
        historial_user_chat_path = None
        try:
            current_historial: ChatHistorial = self.load(user_id, chat_id)
            if reacted_to_profiling_step:
                current_historial.reacted_to_profiling_step = True
            if is_reaction_positive:
                current_historial.is_reaction_positive = True
            if system_profile_set:
                current_historial.system_profile_set = True
            if new_prompt:
                current_historial.messages.append(new_prompt)
            if new_response:
                current_historial.messages.append(new_response)
            historial_user_chat_path = self.path_handler.compose_path(
                [
                    *self.path_components,
                    user_id,
                    f"{chat_id}{Extensions.DOT_JSON.value}",
                ]
            )
            self.file_handler.save(current_historial.dict(), historial_user_chat_path)
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

    def exists(self, user_id: str, chat_id: str) -> bool:
        """Check if an specific chat file exists.

        Args:
            user_id (str): user_id
            chat_id (str): chat_id
        Returns:
            bool: True, otherwise False
        """
        chat_path = self.path_handler.compose_path(
            [
                *self.path_components,
                user_id,
            ]
        )
        return self.path_handler.file_exists(
            chat_path, f"{chat_id}{Extensions.DOT_JSON.value}"
        )

    def create(self, user_id: str, channel_id: str, message_id: str) -> Path:
        """Creates a new ChatHistorial

        Args:
            user_id (str): user_id
            channel_id (str): channel_id
            message_id (str): message_id

        Raises:
            v_e: Pydantic Validation error.
            o_e: OS Error over directory/file operations.

        Returns:
            Path: the Path object with the file full path.
        """
        try:
            chat_id = channel_id
            new_chat_historial = ChatHistorial(
                id=chat_id, message_to_react_id=message_id
            )
            parent_dir = self.path_handler.compose_path(
                [
                    *self.path_components,
                    user_id,
                ]
            )
            self.path_handler.create_directory(parent_dir)
            new_chat_historial_path = self.path_handler.compose_path(
                [
                    *self.path_components,
                    user_id,
                    f"{chat_id}{Extensions.DOT_JSON.value}",
                ]
            )
            self.file_handler.save(new_chat_historial.dict(), new_chat_historial_path)
        except ValidationError as v_e:
            logger.error(v_e)
            raise v_e
        except OSError as o_e:
            logger.error(o_e)
            raise o_e
        return new_chat_historial_path
