import argparse
import sys
import os
from src.repository import fetch_packages_file, parse_package_dependencies # Импорт модуля Этапа 2

def validate_url_or_path(value):
    if value.startswith("http://") or value.startswith("https://"):
        return value
    elif os.path.exists(value):
        return value
    else:
        raise argparse.ArgumentTypeError(f"Путь '{value}' не существует и не является URL.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 2: Сбор данных)"
    )
    parser.add_argument("--package", "-p", required=True, type=str, help="Имя анализируемого пакета")
    parser.add_argument("--repo", "-r", required=True, type=validate_url_or_path, help="URL-адрес репозитория")
    parser.add_argument("--mode", "-m", required=True, choices=["real", "test"], help="Режим работы")
    parser.add_argument("--version", "-v", required=True, type=str, help="Версия пакета")
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
        
        
        if args.mode == "real":
            
            content = fetch_packages_file(args.repo)
            
            
            deps = parse_package_dependencies(content, args.package, args.version)
            
            
            if deps is None:
                print(f"[Ошибка] Пакет '{args.package}' версии '{args.version}' не найден.")
            elif not deps:
                print(f"У пакета '{args.package}' нет прямых зависимостей.")
            else:
                print(f"Прямые зависимости для {args.package} ({args.version}):")
                for d in deps:
                    print(f" - {d}")
        else:
            print("Режим 'test' будет реализован на Этапе 3.")
            
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()