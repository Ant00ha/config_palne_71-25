import os


def generate_plantuml_code(graph, package_name):
    """Генерирует текст PlantUML-диаграммы для графа."""
    lines = [
        "@startuml",
        f"title Dependency Graph for {package_name}",
        "skinparam linetype ortho"
    ]
    
    for pkg, deps in graph.items():
        if not deps:
            lines.append(f'  [{pkg}]')
        else:
            for dep in deps:
                lines.append(f'  [{pkg}] --> [{dep}]')
                
    lines.append("@enduml")
    return "\n".join(lines)


def save_and_open_graph(graph, package_name, filename="graph.puml"):
    """Сохраняет PlantUML код в файл и пытается открыть его."""
    print("Генерация кода PlantUML...")
    puml_code = generate_plantuml_code(graph, package_name)
    
    print("\n--- Код PlantUML ---")
    print(puml_code)
    print("--------------------\n")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(puml_code)
        
    print(f"Файл сохранен: {filename}")
    
    try:
        os.startfile(filename)
        print("Файл открыт в программе по умолчанию.")
    except Exception as e:
        print(f"Не удалось автоматически открыть файл: {e}")
        print("Откройте его вручную в VS Code.")