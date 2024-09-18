import logging
from logging.handlers import TimedRotatingFileHandler


def get_logger(name, config):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.debug('logger has handlers')
        return logger
    level = config.get('logging', {}).get('level', 'INFO').upper()
    logger.setLevel(getattr(logging, level))
    formatter = logging.Formatter(config.get('logging', {}).get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    consoleHeader = logging.StreamHandler()
    consoleHeader.setFormatter(formatter)
    logger.addHandler(consoleHeader)
    file = config.get('logging', {}).get('file', None)
    if file:
        # add file handler
        # make sure the directory exists
        import os
        dir = os.path.dirname(file)
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_handler = TimedRotatingFileHandler(file, when='D', interval=1, backupCount=7, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.debug(f'log file: {file}')
    return logger
