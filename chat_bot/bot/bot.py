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


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


bot.run(os.getenv("DISCORD_BOT_TOKEN"), log_handler=None)
