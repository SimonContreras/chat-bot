"""
OS Path utility class
"""
from pathlib import Path
from typing import List
from chat_bot.utils.logger import logger


class PathHandler:
    """
    A class for common file system operations using the pathlib library.
    """

    @staticmethod
    def create_directory(path: str | Path) -> None:
        """
        Creates a directory at the given path if it does not exist.

        Args:
            path (str | Path): The path to create the directory at.

        Returns:
            None
        """
        path = PathHandler.get_path(path)
        if not path.exists():
            path.mkdir(parents=True)

    @staticmethod
    def delete_directory(path: str | Path) -> None:
        """
        Deletes a directory at the given path if it exists.

        Args:
            path (str | Path): The path to delete the directory from.

        Returns:
            None
        """
        path = PathHandler.get_path(path)
        if path.exists():
            path.rmdir()

    @staticmethod
    def list_directory_files(path: str | Path) -> list[str]:
        """
        Returns a list of file names in the given directory path.

        Args:
            path (str | Path): The directory path to list files from.

        Returns:
            List of file names in the directory.
        """
        path = PathHandler.get_path(path)
        return [file.name for file in path.iterdir() if file.is_file()]

    @staticmethod
    def list_directory_directories(path: str | Path) -> list[str]:
        """
        Returns a list of subdirectory names in the given directory path.

        Args:
            path (str | Path): The directory path to list subdirectories from.

        Returns:
            List of subdirectory names in the directory.
        """
        path = PathHandler.get_path(path)
        return [dir.name for dir in path.iterdir() if dir.is_dir()]

    @staticmethod
    def file_exists(path: str | Path, file_name: str) -> bool:
        """
        Checks if a file exists in the given directory path.

        Args:
            path (str | Path): The directory path to check for the file.
            file_name (str): The name of the file to check for.

        Returns:
            True if the file exists, False otherwise.
        """
        path = PathHandler.get_path(path)
        file_path = path / file_name
        return file_path.exists() and file_path.is_file()

    @staticmethod
    def directory_exists(path: str | Path, directory_name: str) -> bool:
        """
        Checks if a subdirectory exists in the given directory path.

        Args:
            path (str | Path): The directory path to check for the subdirectory.
            directory_name (str): The name of the subdirectory to check for.

        Returns:
            True if the subdirectory exists, False otherwise.
        """
        path = PathHandler.get_path(path)
        dir_path = path / directory_name
        return dir_path.exists() and dir_path.is_dir()

    @staticmethod
    def get_path(path: str | Path) -> Path:
        """Returns a Path object from str | a same Path

        Args:
            path (str | Path): str to return as Path.

        Raises:
            TypeError: wrong parameter type.

        Returns:
            Path: Path object
        """
        path_obj = None
        if isinstance(path, str):
            path_obj = Path(path)
        elif isinstance(path, Path):
            path_obj = path
        else:
            type_error = TypeError("Path must be a string | Path object.")
            logger.error(type_error)
            raise type_error
        return path_obj

    @staticmethod
    def compose_path(components: List[str]) -> Path:
        """Based on a list of strings returns
        a Path object build with the items on the
        same order of the item list.

        Args:
            components (List[str]): items to compose the path.

        Returns:
            Path: a Path object.
        """
        path = Path("/")
        for component in components:
            path /= component
        return path
