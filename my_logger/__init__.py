import os
import time
import logging
from logging import Formatter, Logger, StreamHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class MyLogger(Logger):

    def __init__(
            self,
            name: str = "my-logger",
            is_utc: bool = True,
            level: int or str = logging.INFO,
    ):
        super().__init__(name, self._get_level(level))
        self._formatter = MyLoggerFormatter(is_utc)
        self._add_default_handler()

    @staticmethod
    def _get_level(level: int or str) -> str:
        # Environemt variable LOG_LEVEL takes precedence over the parameter level
        return os.getenv("LOG_LEVEL", level)

    def _add_default_handler(self) -> None:
        stderr_handler = StreamHandler()
        stderr_handler.setFormatter(self._formatter)
        self.addHandler(stderr_handler)

    def add_timed_rotating_file_handler(
            self,
            file_path: str = None,
            interval: int = 7,
            time_unit: str = "d",
            backup_count: int = 7,
            encoding: str = "utf8",
            level: int or str = None,
    ) -> None:
        file_handler = TimedRotatingFileHandler(
            filename=file_path or f"./{self.name}.log",
            interval=interval,
            when=time_unit,
            backupCount=backup_count,
            encoding=encoding,
        )
        file_handler.setFormatter(self._formatter)
        file_handler.setLevel(level or self.level)
        self.addHandler(file_handler)


class MyLoggerFormatter(Formatter):

    def __init__(self, is_utc: bool):
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(parent_dir)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt="%m-%d-%y %H:%M:%S%z %Z",
        )
        self.converter = time.gmtime if is_utc else time.localtime

    # Overrides Formatter's method
    def format(self, record: logging.LogRecord) -> str:
        self._add_parent_dir(record)
        return super().format(record)

    @staticmethod
    def _add_parent_dir(record: logging.LogRecord) -> None:
        file_path = Path(record.pathname)
        # Attaches parent dir name to the log record
        record.parent_dir = file_path.parent.name


logger = MyLogger()
