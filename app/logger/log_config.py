import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(level=logging.INFO, log_file='app/logger/logs/app.log'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    watchfiles_logger = logging.getLogger('watchfiles.main')
    watchfiles_logger.setLevel(logging.WARNING)

    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(name)s:%(lineno)d %(levelname)-7s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Очищаем лог при запуске
    file_handler = RotatingFileHandler(log_file, mode='w', maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    root_logger.handlers.clear()
    
    root_logger.addHandler(file_handler)
