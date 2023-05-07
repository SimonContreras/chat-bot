"""
File handlers util classes
"""
import json
from pathlib import Path
from typing import Dict, Any, Union

from chat_bot.utils.logger import logger
from chat_bot.utils.enums import Encodings


class JsonHandler:
    """
    Json file utility class
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def load(
        full_path: Union[str, Path], encoding: str = Encodings.UTF_8.value
    ) -> Dict[str, Any]:
        """Load a json file using an specific encoding.

        Args:
            full_path (Union[str, Path]): full path to the file to be loaded.
            encoding (str, optional):Encoding to be used to open the file.
                                    Defaults to Encodings.UTF_8.value.

        Raises:
            f_e: File not found found.
            j_e: File with syntax JSON non-compatible.
            v_e: File contains data that cannot be deserialized.

        Returns:
            Dict[str, Any]: A deserialized version of the JSON file, otherwise None
        """
        data = None
        try:
            with open(full_path, "r", encoding=encoding) as file:
                data = json.load(file)
            logger.info(f"File load sucessfully!: {full_path}")
        except FileNotFoundError as f_e:
            logger.error(f_e)
            raise f_e
        except json.JSONDecodeError as j_e:
            logger.error(j_e)
            raise j_e
        except ValueError as v_e:
            logger.error(v_e)
            raise v_e
        return data

    @staticmethod
    def save(
        data: Dict[str, Any],
        full_path: str,
        encoding: str = Encodings.UTF_8.value,
        indent: str = 4,
    ) -> bool:
        """Save a dict-like object to a json file.

        Args:
            data (Dict[str, Any]): Dict-like object to be serialized.
            full_path (str): full path where to save the file.
            encoding (str, optional): Enconding used to write file.
                                    Defaults to Encodings.UTF_8.value.
            indent (str, optional): identation of the file. Defaults to 4.

        Raises:
            f_e: File where to store doesn't exists.
            t_e: Incompatible data object.
            o_e: OS related errors during writing process.

        Returns:
            bool: True file was saved succcesfully, otherwise False.
        """
        is_saved = False
        try:
            with open(full_path, "w", encoding=encoding) as file:
                json.dump(data, file, indent=indent)
            is_saved = True
            logger.info(f"File saved sucessfully!: {full_path}")
        except FileNotFoundError as f_e:
            logger.error(f_e)
            raise f_e
        except TypeError as t_e:
            logger.error(t_e)
            raise t_e
        except OSError as o_e:
            logger.error(o_e)
            raise o_e
        return is_saved
