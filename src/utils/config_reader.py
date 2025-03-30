# src/utils/config_reader.py

import configparser
import os

def read_config(config_file="config/config.ini"):
    """
    Читает конфигурационный файл.

    Args:
        config_file (str): Путь к конфигурационному файлу.

    Returns:
        configparser.ConfigParser: Объект ConfigParser с прочитанными настройками.

    Raises:
        FileNotFoundError: Если файл конфигурации не найден.
    """
    config = configparser.ConfigParser()

    # Проверяем, существует ли файл
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_file}")

    config.read(config_file)
    return config

if __name__ == '__main__':
    # Пример использования (для тестирования)
    try:
        config = read_config()
        print("Конфигурация успешно прочитана:")
        for section in config.sections():
            print(f"[{section}]")
            for key, value in config.items(section):
                print(f"  {key} = {value}")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")