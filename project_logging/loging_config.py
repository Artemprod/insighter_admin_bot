from environs import Env
from logtail import LogtailHandler
from loguru import logger
import os


def find_file(filename, search_path):
    """Поиск файла в указанной директории и её поддиректориях.

    Args:
    filename (str): Имя файла для поиска.
    search_path (str): Путь к директории, откуда начать поиск.

    Returns:
    str: Полный путь к найденному файлу или None, если файл не найден.
    """
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def load_loguru():
    file_path = os.path.normpath(find_file('.env', '../'))
    if file_path:
        print(f'Файл найден: {file_path}')
        env: Env = Env()
        env.read_env(file_path)
        logtail_source_token = env("LOGTAIL_INSIGHTER_ADMIN_SOURCE")
        logtail_handler = LogtailHandler(source_token=logtail_source_token)
        logger.add(
            logtail_handler,
            format="{message}",
            level="INFO",
            backtrace=False,
            diagnose=False,
        )
        return logger
    else:
        print('Файл не найден.')


loguru_main_logger = load_loguru()
