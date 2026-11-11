import argparse
import sys
import os
from src.repository import fetch_packages_file, parse_package_dependencies
from src.graph import parse_test_graph, build_dependency_graph

def validate_url_or_path(value):
    if value.startswith("http://") or value.startswith("https://"):
        return value
    elif os.path.exists(value):
        return value
    else:
        raise argparse.ArgumentTypeError(f"Путь '{value}' не существует и не является URL.")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 3: Граф)"
    )
    parser.add_argument("--package", "-p", required=True, type=str, help="Имя анализируемого пакета")
    parser.add_argument("--repo", "-r", required=True, type=validate_url_or_path, help="URL репозитория или путь к тестовому файлу")
    parser.add_argument("--mode", "-m", required=True, choices=["real", "test"], help="Режим работы")
    parser.add_argument("--version", "-v", required=True, type=str, help="Версия пакета (используется только в real mode)")
    return parser.parse_args()

def get_real_dependencies(package_name, repo_url, version, cache_dict):
    if not cache_dict:
        print("Загрузка базы данных репозитория...")
        content = fetch_packages_file(repo_url)
        cache_dict['raw_content'] = content

    deps = parse_package_dependencies(cache_dict['raw_content'], package_name, version)
    return deps if deps is not None else []

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
            repo_cache = {}
            
            def fetch_wrapper(pkg_name):
                return get_real_dependencies(pkg_name, args.repo, args.version, repo_cache)

            graph = build_dependency_graph(args.package, fetch_wrapper, is_test_mode=False)
            
        else:
            test_graph_data = parse_test_graph(args.repo)
            graph = build_dependency_graph(args.package, None, is_test_mode=True, test_graph=test_graph_data)

        print("\n--- Результат (Граф зависимостей) ---")
        if not graph:
            print("Граф пуст.")
        else:
            for pkg, deps in graph.items():
                print(f"{pkg} -> {', '.join(deps) if deps else '[]'}")

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()