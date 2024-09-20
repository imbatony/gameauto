import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Logger
from colorlog import ColoredFormatter


def get_logger(name, config) -> Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers() and hasattr(logger, "initialized"):
        return logger
    logger.propagate = False
    level = config.get("logging", {}).get("level", "INFO").upper()
    logger.setLevel(getattr(logging, level))
    consoleHeader = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s\t%(filename)s:%(lineno)d - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "purple",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    consoleHeader.setFormatter(formatter)
    logger.addHandler(consoleHeader)
    file = config.get("logging", {}).get("file", None)
    if file:
        # add file handler
        # make sure the directory exists
        import os

        dir = os.path.dirname(file)
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_handler = TimedRotatingFileHandler(
            file, when="D", interval=1, backupCount=7, encoding="utf-8"
        )
        formatter = logging.Formatter(
            config.get("logging", {}).get(
                "format", "%(levelname)8s\t%(asctime)s\t%(filename)-15s\t%(message)s"
            )
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.initialized = True
    return logger
