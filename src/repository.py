import urllib.request
import urllib.error
import gzip


def fetch_packages_file(repo_url):
    """Скачивает файл Packages (или Packages.gz) по URL."""
    print(f"Скачивание данных из: {repo_url} ...")
    
    try:
        req = urllib.request.Request(
            repo_url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (DependencyVisualizer/1.0)'
            }
        )
        
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        if repo_url.endswith('.gz') or data[:2] == b'\x1f\x8b':
            print("Обнаружен сжатый файл (gzip). Распаковка...")
            data = gzip.decompress(data)
            
        return data.decode('utf-8')
        
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Ошибка сети при скачивании {repo_url}: {e}"
        )
    except Exception as e:
        raise RuntimeError(f"Ошибка обработки файла: {e}")


def _extract_package_fields(block):
    """Извлекает имя, версию и строку зависимостей из блока."""
    pkg_name = None
    pkg_version = None
    depends_line = None
    
    for line in block.split('\n'):
        if line.startswith('Package: '):
            pkg_name = line[len('Package: '):].strip()
        elif line.startswith('Version: '):
            pkg_version = line[len('Version: '):].strip()
        elif line.startswith('Depends: '):
            depends_line = line[len('Depends: '):].strip()
            
    return pkg_name, pkg_version, depends_line


def _parse_depends_string(depends_line):
    """Превращает строку 'Depends: ...' в список имен пакетов."""
    if not depends_line:
        return []
    
    deps = []
    for dep in depends_line.split(','):
        dep = dep.strip()
        clean_dep = dep.split('(')[0].split('|')[0].strip()
        if clean_dep:
            deps.append(clean_dep)
    return deps


def parse_package_dependencies(packages_text, target_package, target_version):
    """Ищет пакет и версию в тексте, возвращает список зависимостей."""
    blocks = packages_text.strip().split('\n\n')
    
    for block in blocks:
        name, version, depends = _extract_package_fields(block)
        
        if name == target_package and version == target_version:
            return _parse_depends_string(depends)
            
    return None