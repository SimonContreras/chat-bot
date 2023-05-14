"""Discord bot logger configs"""
from logging import Formatter, StreamHandler, getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from chat_bot.utils.logger import logger

dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = Formatter("[{asctime}] [{levelname}] {name}: {message}", dt_fmt, style="{")

discord_logger = getLogger("discord")
discord_logger.setLevel(DEBUG)

discord_file_handler = RotatingFileHandler(
    filename="discord.log",
    encoding="utf-8",
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
discord_file_handler.setFormatter(formatter)
discord_logger.addHandler(discord_file_handler)

discord_stdout_handler = StreamHandler()
discord_stdout_handler.setFormatter(formatter)
discord_logger.addHandler(discord_stdout_handler)


class DiscordLoggerSink:
    """Sink to make compatible with loguru"""

    def write(self, message: str):
        """method called from loguru to write message

        Args:
            message (str): message to show
        """
        if message.strip():
            discord_logger.debug(message.strip())


discord_logger_sink = DiscordLoggerSink()
logger.add(
    discord_logger_sink,
    colorize=True,
    backtrace=True,
    diagnose=True,
)
