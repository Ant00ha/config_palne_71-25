import os
import subprocess

def generate_plantuml_code(graph, package_name):
    lines = []
    lines.append("@startuml")
    lines.append(f"title Dependency Graph for {package_name}")
    lines.append("skinparam linetype ortho")
    
    for pkg, deps in graph.items():
        if not deps:
            lines.append(f'  [{pkg}]')
        else:
            for dep in deps:
                lines.append(f'  [{pkg}] --> [{dep}]')
                
    lines.append("@enduml")
    return "\n".join(lines)

def save_and_open_graph(graph, package_name, filename="graph.puml"):
    print("Генерация кода PlantUML...")
    puml_code = generate_plantuml_code(graph, package_name)
    
    print("\n--- Код PlantUML ---")
    print(puml_code)
    print("--------------------\n")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(puml_code)
        
    print(f"Файл сохранен: {filename}")
    
    # Пытаемся открыть файл через системный редактор (обычно это VS Code или Notepad)
    # Если у вас установлено расширение PlantUML в VS Code, он покажет картинку.
    try:
        os.startfile(filename)
        print("Файл открыт в программе по умолчанию. Если вы используете VS Code с расширением PlantUML, вы увидите диаграмму.")
    except Exception as e:
        print(f"Не удалось автоматически открыть файл: {e}")
        print("Откройте его вручную в VS Code (нужно расширение PlantUML).")