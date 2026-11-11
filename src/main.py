import argparse
import sys
import os

def validate_url_or_path(value):
    """
    Проверяет, является ли строка URL-адресом или существующим путем.
    """
    if value.startswith("http://") or value.startswith("https://"):
        return value
    elif os.path.exists(value):
        return value
    else:
        raise argparse.ArgumentTypeError(f"Путь '{value}' не существует и не является URL.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 1: Конфигурация)"
    )

    # имя пакета
    parser.add_argument(
        "--package", "-p",
        required=True,
        type=str,
        help="Имя анализируемого пакета (например, bash)"
    )

    # url репозитория или путь к файлу
    parser.add_argument(
        "--repo", "-r",
        required=True,
        type=validate_url_or_path,
        help="URL-адрес репозитория или путь к файлу тестового репозитория"
    )

    # режим работы
    parser.add_argument(
        "--mode", "-m",
        required=True,
        choices=["real", "test"],
        help="Режим работы с репозиторием: 'real' (URL) или 'test' (локальный файл)"
    )

    # версия пакета
    parser.add_argument(
        "--version", "-v",
        required=True,
        type=str,
        help="Версия пакета (например, 5.0-4ubuntu1)"
    )

    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        
        
        print("--- Параметры конфигурации ---")
        print(f"package_name: {args.package}")
        print(f"repository_url: {args.repo}")
        print(f"mode: {args.mode}")
        print(f"package_version: {args.version}")
        print("------------------------------")
        
        print("Этап 1 успешно завершен. Параметры приняты.")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()