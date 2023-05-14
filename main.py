"main file to run discord bot"
from chat_bot.bot.bot import bot
from chat_bot.bot.utils.configs import DISCORD_SETTINGS


if __name__ == "__main__":
    bot.run(DISCORD_SETTINGS.DISCORD_BOT_TOKEN, log_handler=None)
