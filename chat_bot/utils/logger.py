"""
Logger config file
"""
from sys import stderr
from logging import INFO

from loguru import logger


logger.add(
    sink=stderr,
    level=INFO,
    format="[{time} | {level}] - {message}",
    colorize=True,
    backtrace=True,
    diagnose=True,
)
logger.add(sink="dev_logs.log", rotation="500 MB", compression="zip")
