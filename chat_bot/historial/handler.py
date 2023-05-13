"""
History handler class to load and save chat historial
"""
from uuid import uuid4
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

    def save(
        self, user_id: str, chat_id: str, new_prompt: Message, new_response: Message
    ) -> bool:
        """Update existing ChatHistorial with the new prompt and the correponding
        API response.

        Args:
            user_id (str): user id.
            chat_id (str): chat id.
            new_prompt (Message): New prompt to be saved.
            new_response (Message): New response to be saved.

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
            current_historial.messages.append(new_prompt)
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

    def create(
        self, user_id: str, system_profiling: Message, assistant_response: Message
    ) -> Path:
        """Creates a new ChatHistorial

        Args:
            user_id (str): user_id
            system_profiling (Message): Profile defined for the chat.
            assistant_response (Message): Response of the API about the profiling request sent.

        Raises:
            v_e: Pydantic Validation error.
            o_e: OS Error over directory/file operations.

        Returns:
            Path: the Path object with the file full path.
        """
        try:
            chat_id = str(uuid4())
            new_chat_historial = ChatHistorial(
                id=chat_id, messages=[system_profiling, assistant_response]
            )
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