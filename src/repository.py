import urllib.request
import urllib.error
import gzip

def fetch_packages_file(repo_url):
    """
    Скачивает файл Packages (или Packages.gz) по указанному URL.
    Возвращает текст в виде строки.
    """
    print(f"Скачивание данных из: {repo_url} ...")
    
    try:# Добавляем User-Agent, чтобы сервер Ubuntu не блокировал запрос
        req = urllib.request.Request(
            repo_url, 
            headers={'User-Agent': 'Mozilla/5.0 (DependencyVisualizer/1.0)'}
        )
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        # Проверяем, сжат ли файл (по расширению или по магическим байтам gzip)
        if repo_url.endswith('.gz') or data[:2] == b'\x1f\x8b':
            print("Обнаружен сжатый файл (gzip). Распаковка...")
            data = gzip.decompress(data)
            
        return data.decode('utf-8')
        
    except urllib.error.URLError as e:
        raise RuntimeError(f"Ошибка сети при скачивании {repo_url}: {e}")
    except Exception as e:
        raise RuntimeError(f"Ошибка обработки файла: {e}")

def parse_package_dependencies(packages_text, target_package, target_version):
    """
    Ищет нужный пакет и версию в тексте, извлекает поле Depends.
    Возвращает список зависимостей или None, если пакет не найден.
    """
    # Файл Packages состоит из блоков, разделенных двумя переносами строки (\n\n)
    blocks = packages_text.strip().split('\n\n')
    
    for block in blocks:
        lines = block.split('\n')
        pkg_name = None
        pkg_version = None
        depends_line = None
        
        for line in lines:
            if line.startswith('Package: '):
                pkg_name = line[len('Package: '):].strip()
            elif line.startswith('Version: '):
                pkg_version = line[len('Version: '):].strip()
            elif line.startswith('Depends: '):
                depends_line = line[len('Depends: '):].strip()
                
        # Проверяем совпадение имени и версии
        if pkg_name == target_package and pkg_version == target_version:
            if not depends_line:
                return [] # Зависимостей нет
            
            deps = []
            # Строка зависимостей выглядит так: "libc6 (>= 2.34), libtinfo6 (>= 6) | libtinfo5"
            for dep in depends_line.split(','):
                dep = dep.strip()
                # Убираем версию в скобках и альтернативные варианты (через |)
                clean_dep = dep.split('(')[0].split('|')[0].strip()
                if clean_dep:
                    deps.append(clean_dep)
            return deps
            
    return None