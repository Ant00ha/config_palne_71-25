import os

def parse_test_graph(file_path):
    graph = {}
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Тестовый файл не найден: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ':' in line:
                pkg, deps_str = line.split(':', 1)
                pkg = pkg.strip()
                deps = [d.strip() for d in deps_str.split(',') if d.strip()]
                graph[pkg] = deps
            else:
                graph[line] = []
    return graph

def build_dependency_graph(start_package, fetcher_func, is_test_mode=False, test_graph=None):
    full_graph = {}
    stack = [start_package]
    visited = set()

    print(f"Построение графа зависимостей (DFS) для '{start_package}'...")

    while stack:
        current_package = stack.pop()
        
        if current_package in visited:
            continue
            
        visited.add(current_package)
        
        deps = []
        if is_test_mode:
            if test_graph and current_package in test_graph:
                deps = test_graph[current_package]
            else:
                deps = []
        else:
            deps = fetcher_func(current_package) or []
            
        full_graph[current_package] = deps
        
        for dep in reversed(deps):
            if dep not in visited:
                stack.append(dep)

    return full_graph

def build_reverse_graph(graph):
    reverse_graph = {}
    
    for pkg, deps in graph.items():
        if pkg not in reverse_graph:
            reverse_graph[pkg] = []
            
        for dep in deps:
            if dep not in reverse_graph:
                reverse_graph[dep] = []
            reverse_graph[dep].append(pkg)
            
    return reverse_graph

def get_reverse_dependencies(target_package, graph, is_test_mode=False, fetcher_func=None):
    print(f"Поиск обратных зависимостей для '{target_package}'...")
    result = []
    
    if is_test_mode:
        reverse_graph = build_reverse_graph(graph)
        if target_package in reverse_graph:
            stack = list(reverse_graph[target_package])
            visited = set()
            
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                result.append(current)
                
                if current in reverse_graph:
                    for parent in reverse_graph[current]:
                        if parent not in visited:
                            stack.append(parent)
        return result

    else:
        print("Анализ всех пакетов в репозитории для поиска обратных зависимостей...")
        for pkg, deps in graph.items():
            if target_package in deps:
                result.append(pkg)
        return result