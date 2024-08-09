"""
Defines the "Log" class, used to save logs of the program inside a specified file.
"""

__all__ = ["Log"]

__author__ = "Valerio Molinari"
__credits__ = "Valerio Molinari"
__maintainer__ = "Valerio Molinari"
__email__ = "valeriomolinariprogrammazione@gmail.com"

from datetime import datetime


class Log:
    def __init__(self, path: str):
        """This class provides methods for managing the registration of logs to
        a specific log-file. The format of logs is:

        [dd-mm-yy hh-mm-ss] - Log data

        :param path: the path to the log-file
        """
        self.path = path

    def write(self, string: str) -> None:
        """Writes a new log to the log-file.

        :param string: log's data
        """
        with open(self.path, 'a') as log:
            log.write(f'{self.now()} - {string}\n')

    def newline(self):
        """An utility to write a new line to the log-file."""
        with open(self.path, 'a') as log:
            log.write('\n')

    @staticmethod
    def now() -> str:
        """Return a representation of the moment when its called
        as a string.

        :return: [dd-mm-yyyy hh-mm-ss]
        """
        return datetime.now().strftime("[%d-%m-%Y %H-%M-%S]")
