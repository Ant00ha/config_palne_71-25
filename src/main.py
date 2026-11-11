import argparse
import sys
import os
from src.repository import fetch_packages_file, parse_package_dependencies
from src.graph import (
    parse_test_graph,
    build_dependency_graph,
    get_reverse_dependencies
)
from src.visualizer import save_and_open_graph


def validate_url_or_path(value):
    """Проверяет, что введен URL или существующий путь."""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if os.path.exists(value):
        return value
    raise argparse.ArgumentTypeError(
        f"Путь '{value}' не существует и не является URL."
    )


def parse_arguments():
    """Настраивает и парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей"
    )
    parser.add_argument(
        "--package", "-p", required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo", "-r", required=True,
        type=validate_url_or_path,
        help="URL репозитория или путь к тестовому файлу"
    )
    parser.add_argument(
        "--mode", "-m", required=True,
        choices=["real", "test"], help="Режим работы"
    )
    parser.add_argument(
        "--version", "-v", required=True,
        help="Версия пакета"
    )
    parser.add_argument(
        "--reverse", "-rv", action="store_true",
        help="Показать обратные зависимости"
    )
    parser.add_argument(
        "--visualize", "-vis", action="store_true",
        help="Открыть граф в PlantUML"
    )
    return parser.parse_args()


def get_real_dependencies(pkg_name, repo_url, version, cache_dict):
    """Получает зависимости для реального пакета с кэшированием."""
    if not cache_dict:
        print("Загрузка базы данных репозитория...")
        content = fetch_packages_file(repo_url)
        cache_dict['raw_content'] = content

    deps = parse_package_dependencies(
        cache_dict['raw_content'], pkg_name, version
    )
    return deps if deps is not None else []


def build_graph(args):
    """Строит граф зависимостей в зависимости от режима."""
    if args.mode == "real":
        repo_cache = {}

        def fetch_wrapper(pkg_name):
            return get_real_dependencies(
                pkg_name, args.repo, args.version, repo_cache
            )

        return build_dependency_graph(
            args.package, fetch_wrapper, is_test_mode=False
        )
    
    test_graph_data = parse_test_graph(args.repo)
    return build_dependency_graph(
        args.package, None, is_test_mode=True, test_graph=test_graph_data
    )


def print_reverse_dependencies(args, graph):
    """Выводит обратные зависимости."""
    reverse_deps = get_reverse_dependencies(
        args.package, graph, is_test_mode=(args.mode == "test")
    )
    print("\n--- Результат (Обратные зависимости) ---")
    if not reverse_deps:
        print(f"Пакеты, зависящие от '{args.package}', не найдены.")
    else:
        print(f"Пакеты, которые зависят от {args.package}:")
        for dep in reverse_deps:
            print(f" - {dep}")


def print_graph(args, graph):
    """Выводит граф и запускает визуализацию при необходимости."""
    print("\n--- Результат (Граф зависимостей) ---")
    if not graph:
        print("Граф пуст.")
        return

    for pkg, deps in graph.items():
        deps_str = ', '.join(deps) if deps else '[]'
        print(f"{pkg} -> {deps_str}")
        
    if args.visualize:
        save_and_open_graph(graph, args.package)


def main():
    """Точка входа в программу."""
    try:
        args = parse_arguments()
        
        print("--- Параметры конфигурации ---")
        print(f"package_name: {args.package}")
        print(f"repository_url: {args.repo}")
        print(f"mode: {args.mode}")
        print(f"package_version: {args.version}")
        print("------------------------------")
        
        graph = build_graph(args)

        if args.reverse:
            print_reverse_dependencies(args, graph)
        else:
            print_graph(args, graph)

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()