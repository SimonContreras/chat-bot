"""
Class to interact with openai API
"""
from copy import deepcopy
from uuid import uuid4
import openai
from openai.openai_object import OpenAIObject
from openai.error import AuthenticationError
from pydantic import ValidationError
from chat_bot.utils.logger import logger
from chat_bot.utils.enums import Engines, Roles
from chat_bot.models.message import Message
from chat_bot.models.user import User
from chat_bot.models.response import ChatCompletionResponse
from chat_bot.historial.handler import ChatHistorialHandler
from chat_bot.models.historial import ChatHistorial


class OpenAiApi:
    """
    Core class to connect to OpenAI API
    """

    def __init__(
        self,
        token: str,
        user: User,
        model: str = Engines.GPT_3_5_TURBO.value,
        chat_historial_handler: ChatHistorialHandler = ChatHistorialHandler(),
    ) -> None:
        self.api = openai
        self.api.api_key = token
        self.user = user
        self.model = model
        self.chat_historial_handler = chat_historial_handler
        self._test_token()
        logger.info("OpenApi client created!")

    def _test_token(self) -> bool:
        status = False
        prompt = "Just trying the token validity via an api call"
        message = Message(
            role=Roles.USER.value, content=prompt, name=self.user.username
        )
        try:
            self.api.ChatCompletion.create(
                model=self.model, messages=[message.dict()], max_tokens=5
            )
            status = True
        except AuthenticationError as a_e:
            logger.error(a_e)
            raise a_e
        return status

    def _consolidate_messages(
        self, historial_messages: ChatHistorial, new_message: Message
    ) -> ChatHistorial:
        """Add a new message at the end of the ChatHistorial

        Args:
            historial_messages (ChatHistorial): ChatHistorial loaded on pydantic model.
            new_message (Message): new Message to be added
        Raises:
            v_e: A validation error occurs.
        Returns:
            ChatHistorial: ChatHistorial object updated, otherwise None.
        """
        consolidated_messages = None
        try:
            if historial_messages:
                historial_messages.messages.append(new_message)
                consolidated_messages = deepcopy(historial_messages)
            else:
                consolidated_messages = ChatHistorial(
                    id=str(uuid4()), messages=[new_message]
                )
        except ValidationError as v_e:
            logger.error(v_e)
            raise v_e
        return consolidated_messages

    def send_chat_completion(
        self,
        chat_id: str,
        content: str,
        role: str = Roles.USER.value,
        save: bool = True,
        use_historial: bool = True,
    ) -> ChatCompletionResponse | None:
        """First version of API call to chat completion, supports chathistorial
        and persistency if the call is succesfull.

        Args:
            chat_id (str): chat internal id.
            content (str): message to be sent.
            role (str, optional): API compatible role. Defaults to Roles.USER.value.
            save (bool, optional): Flag to persistency logic. Defaults to True.
            use_historial (bool, optional):flag to add chat historial. Defaults to True.

        Raises:
            a_e: Authentication error over API.

        Returns:
            ChatCompletionResponse | None: ChatCompetionResponse, otherwise None
        """
        chat_response = None
        historial_messages = None
        new_prompt = Message(role=role, content=content, name=self.user.username)
        try:
            if use_historial:
                historial_messages: ChatHistorial = self.chat_historial_handler.load(
                    self.user.id, chat_id
                )
            consolidated_messages = self._consolidate_messages(
                historial_messages, new_prompt
            )
            response: OpenAIObject = self.api.ChatCompletion.create(
                model=self.model,
                messages=consolidated_messages.dict(exclude_none=True)["messages"],
            )
            chat_response = ChatCompletionResponse.parse_obj(
                response.to_dict_recursive()
            )
            new_response = Message(
                role=Roles.ASSISTANT.value,
                content=chat_response.choices[0].message.content,
                name=None,
            )
        except AuthenticationError as a_e:
            raise a_e

        if save:
            self.chat_historial_handler.save(
                self.user.id, historial_messages.id, new_prompt, new_response
            )
        return chat_response

    # this logic would me moved to the bot cogs or controllers when the user crud logic will be done.
    def resolve_api_call(
        self,
        chat_id: str,
        content: str,
        role: str = Roles.USER.value,
        save: bool = True,
        use_historial: bool = True,
    ):
        if chat_id and self.chat_historial_handler.exists(self.user.id, chat_id):
            self.send_chat_completion(chat_id, content, role, save, use_historial)
        else:
            system_profiling_message = Message(role=Roles.SYSTEM.value, content=content)
            asistant_response = self.send_chat_completion(
                chat_id, content, Roles.SYSTEM.value, False, False
            )
            assistance_response_message = Message(
                role=Roles.ASSISTANT.value,
                content=asistant_response.choices[0].message.content,
                name=None,
            )
            self.chat_historial_handler.create(
                self.user.id, system_profiling_message, assistance_response_message
            )
