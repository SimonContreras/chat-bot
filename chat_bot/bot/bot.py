"""Main bot module"""
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

"""Logger must be imported despite is an unused import"""  # pylint: disable=W0105
from chat_bot.bot.utils.logger import logger  # pylint: disable=C0413,W0611


load_dotenv()

"""This can be narrowed when all the features will be defined"""  # pylint: disable=W0105
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


bot.run(os.getenv("DISCORD_BOT_TOKEN"), log_handler=None)
