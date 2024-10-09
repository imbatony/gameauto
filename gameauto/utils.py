from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Logger
from colorlog import ColoredFormatter

import importlib
import types


def get_logger(name, config) -> Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers() and hasattr(logger, "initialized"):
        return logger
    logger.propagate = False
    debug: bool = config.get("debug", False)
    level = debug and "DEBUG" or "INFO"
    logger.setLevel(getattr(logging, level))
    consoleHeader = logging.StreamHandler()
    console_default_log_format = debug and "%(log_color)s%(levelname)s%(reset)s\t%(pathname)s:%(lineno)d - %(message)s" or "%(log_color)s%(message)s%(reset)s"
    formatter = ColoredFormatter(
        console_default_log_format,
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
        file_handler = TimedRotatingFileHandler(file, when="D", interval=1, backupCount=7, encoding="utf-8")
        formatter = logging.Formatter(config.get("logging", {}).get("format", "%(levelname)8s\t%(asctime)s\t%(filename)-15s\t%(message)s"))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.initialized = True
    return logger


class LazyLoader(types.ModuleType):
    """Lazily import a module, mainly to avoid pulling in large dependencies.

    `contrib`, and `ffmpeg` are examples of modules that are large and not always
    needed, and this allows them to only be loaded when they are used.
    """

    # The lint error here is incorrect.
    def __init__(self, local_name, parent_module_globals, name):  # pylint: disable=super-on-old-class
        self._local_name = local_name
        self._parent_module_globals = parent_module_globals

        super(LazyLoader, self).__init__(name)

    def _load(self):
        # Import the target module and insert it into the parent's namespace
        module = importlib.import_module(self.__name__)
        self._parent_module_globals[self._local_name] = module

        # Update this object's dict so that if someone keeps a reference to the
        #   LazyLoader, lookups are efficient (__getattr__ is only called on lookups
        #   that fail).
        self.__dict__.update(module.__dict__)

        return module

    def __getattr__(self, item):
        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)
