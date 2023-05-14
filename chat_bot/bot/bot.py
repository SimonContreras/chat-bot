"""Main bot module"""
from discord import Intents, RawReactionActionEvent
from discord.ext import commands
from discord.ext.commands.context import Context
from chat_bot.models.message import Message

from chat_bot.models.user import User
from chat_bot.historial.handler import ChatHistorialHandler
from chat_bot.user.handler import UserHandler
from chat_bot.api.chat_gpt import OpenAIApi
from chat_bot.utils.enums import Roles
from chat_bot.utils.configs import OPENAI_SETTINGS


"""Logger must be imported despite is an unused import"""
from chat_bot.bot.utils.logger import logger  # pylint: disable=C0413,W0611
from chat_bot.bot.constants.enums import DefaultMessages, Prefix

"""This can be narrowed when all the features will be defined"""
intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=Prefix.QUESTION_MARK.value, intents=intents)


@bot.command()
async def chat(ctx: Context):
    """Main command for Chat Bot"""
    author_id: str = str(ctx.author.id)
    display_name: str = ctx.author.display_name
    name: str = ctx.author.name
    discriminator: str = ctx.author.discriminator
    message_id: str = str(ctx.message.id)
    message_content: str = ctx.message.content.split("$profile")[-1][1:]
    channel_id: str = str(ctx.channel.id)

    """Check if the current user exists, otherwise creates one o db"""
    user_handler = UserHandler()
    if not user_handler.exists(str(author_id)):
        new_user = User(
            id=author_id,
            display_name=display_name,
            name=name,
            discriminator=discriminator,
        )
        user_handler.create(user=new_user)

    """Check if an historial on this channel exists, otherwise creates one o db"""
    chat_handler = ChatHistorialHandler()
    if not chat_handler.exists(user_id=str(author_id), chat_id=str(channel_id)):
        chat_handler.create(
            user_id=str(author_id), channel_id=str(channel_id), message_id=message_id
        )

        """Sent message to start system profiling step"""
        await ctx.send(DefaultMessages.NO_PROFILING_SET.value.format(author_name=name))

    else:
        """Check if ChatHistorial is empty and if reaction is positive to add system profiling"""
        chat_historial = chat_handler.load(
            user_id=str(author_id), chat_id=str(channel_id)
        )
        if (
            not chat_historial.reacted_to_profiling_step
            and len(chat_historial.messages) == 0
        ):
            await ctx.send(DefaultMessages.REACT_TO_MESSAGE_OTHERWISE_BLOCK.value)

        elif chat_historial.reacted_to_profiling_step:
            await ctx.send(":thinking:")
            user = UserHandler().load(user_id=author_id)
            openai_client = OpenAIApi(token=OPENAI_SETTINGS.OPENAI_API_KEY, user=user)
            api_response = openai_client.send_chat_completion(
                chat_id=channel_id, content=message_content, role=Roles.USER.value
            )
            await ctx.send(api_response.choices[0].message.content)


@bot.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    """Logic to add or not a system profile to the chatbot"""
    channel_id = str(payload.channel_id)
    user_id = str(payload.user_id)
    emoji = payload.emoji
    chat_handler = ChatHistorialHandler()
    channel = bot.get_channel(payload.channel_id)
    if chat_handler.exists(user_id=user_id, chat_id=channel_id):
        chat_historial = chat_handler.load(user_id=user_id, chat_id=channel_id)

        """If reaction is positive, set flag to True and send instruction to send profile
        Otherwise set flag and send feedback message to redirect to use $chat message"""
        if (
            emoji.name == "✅"
            and not chat_historial.is_reaction_positive
            and not chat_historial.reacted_to_profiling_step
        ):
            if chat_handler.update(
                user_id=user_id,
                chat_id=channel_id,
                is_reaction_positive=True,
                reacted_to_profiling_step=True,
            ):
                await channel.send(
                    "Perfecto envia un mensaje con el comando $profile e indica el perfil que quieres que tenga"
                )
                await channel.send("por ejemplo puedo ser un ...")
            else:
                await channel.send("Oops Error!, Contacta a los admins del server")
        elif emoji.name == "❌" and not chat_historial.reacted_to_profiling_step:
            if chat_handler.update(
                user_id=user_id, chat_id=channel_id, reacted_to_profiling_step=True
            ):
                await channel.send(
                    "Perfecto no se seteara un perfil. De ahora en adelante podemos seguir conversando usando el comando $chat"
                )
            else:
                await channel.send("Oops Error!, Contacta a los admins del server")


@bot.command()
async def profile(ctx: Context):
    """Command to set system profile"""
    author_id: str = str(ctx.author.id)
    name: str = ctx.author.name
    message_content: str = ctx.message.content.split("$profile")[-1][1:]
    channel_id: str = str(ctx.channel.id)

    chat_handler = ChatHistorialHandler()
    if chat_handler.exists(user_id=str(author_id), chat_id=str(channel_id)):
        chat_historial = chat_handler.load(user_id=author_id, chat_id=channel_id)
        if (
            chat_historial.is_reaction_positive
            and chat_historial.reacted_to_profiling_step
        ):
            system_role_msg = Message(role=Roles.SYSTEM.value, content=message_content)
            chat_handler.update(
                user_id=author_id,
                chat_id=channel_id,
                new_prompt=system_role_msg,
                system_profile_set=True,
            )
            await ctx.send(f"Ok {name} de ahora actuare como un:  {message_content}")
            await ctx.send(
                "Ya puedes seguir conversando conmigo a traves del comando $chat"
            )

    else:
        await ctx.send("Oops Error!, Contacta a los admins del server")
