"""Main bot module"""
from discord import Intents, Member, TextChannel
from discord.ext import commands
from discord.ext.commands.context import Context

from chat_bot.models.user import User
from chat_bot.historial.handler import ChatHistorialHandler
from chat_bot.user.handler import UserHandler

"""Logger must be imported despite is an unused import"""
from chat_bot.bot.utils.logger import logger  # pylint: disable=C0413,W0611
from chat_bot.bot.constants.enums import DefaultMessages
from chat_bot.bot.utils.configs import DISCORD_SETTINGS

"""This can be narrowed when all the features will be defined"""
intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def chat(ctx: Context):
    """Main command for Chat Bot"""
    author: Member = ctx.author
    author_id: int = author.id
    display_name: str = author.display_name
    name: str = author.name
    discriminator: str = author.discriminator
    message: str = ctx.current_argument
    channel: TextChannel = ctx.channel

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
    if not chat_handler.exists(user_id=str(author_id), chat_id=channel.id):
        chat_handler.create(user_id=str(author_id), channel_id=str(channel.id))

        """Sent message to start system profiling step"""
        await ctx.send(DefaultMessages.NO_PROFILING_SET.value)

    """Check if ChatHistorial is empty and if reaction is positive to add system profiling"""

    """If ChatHistorial have flag reacted_to_step True, following normal api calls, otherwise redirect to reacted to the message"""

    """Check if reaction is positive or negative, probably an on_Reaction event to be implemented,
    check if the profiling can be via interactive box on chat"""
    if message == "si" and chat_handler.exists(
        user_id=str(author_id), chat_id=channel.id
    ):
        pass
    elif message == "no" and chat_handler.exists(
        user_id=str(author_id), chat_id=channel.id
    ):
        pass


bot.run(DISCORD_SETTINGS.DISCORD_BOT_TOKEN, log_handler=None)
