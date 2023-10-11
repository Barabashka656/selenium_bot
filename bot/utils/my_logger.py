import os
import logging
from logging import handlers

def create_handler(log_filename: str) -> handlers.RotatingFileHandler:
    log_folder = os.path.join('bot', 'data', 'logs')
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    log_file = os.path.join(log_folder, log_filename)
    handler = handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=1e7,
        backupCount=5,
        encoding='utf-8'
    )
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    return handler


def configure_root_logger():
    logging.basicConfig(level=logging.INFO)
    handler = create_handler('python_logs.log')
    logging.getLogger().addHandler(handler)


def setup_attempts_logger() -> logging.Logger:
    handler = create_handler('attempts_logs.log')
    logger = logging.getLogger('attempts')
    logger.addHandler(handler)
    return logger