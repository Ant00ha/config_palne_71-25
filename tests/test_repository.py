import unittest
from src.repository import parse_package_dependencies


class TestRepositoryParsing(unittest.TestCase):
    """Тесты для парсера репозитория."""

    def set_up(self):
        """Подготовка тестовых данных."""
        self.mock_packages_text = (
            "Package: bash\n"
            "Version: 5.1-6ubuntu1\n"
            "Architecture: amd64\n"
            "Depends: base-files (>= 1.0), debianutils (>= 1.0), "
            "libc6 (>= 2.34), libtinfo6 (>= 6)\n"
            "Description: GNU Bourne Again SHell\n"
            " Bash is an sh-compatible command language interpreter.\n"
            "\n"
            "Package: coreutils\n"
            "Version: 8.32-4.1ubuntu1\n"
            "Architecture: amd64\n"
            "Depends: libc6 (>= 2.34), libssl3 (>= 3.0.0), "
            "libselinux1 (>= 3.1)\n"
            "Description: GNU core utilities\n"
            " Basic file, shell and text manipulation utilities.\n"
            "\n"
            "Package: no-deps-package\n"
            "Version: 1.0.0\n"
            "Architecture: amd64\n"
            "Description: Package with no dependencies\n"
            " This package has no Depends field.\n"
        )

    def test_parse_existing_package(self):
        """Тест 1: Успешный парсинг пакета с зависимостями."""
        self.set_up()
        deps = parse_package_dependencies(
            self.mock_packages_text, "bash", "5.1-6ubuntu1"
        )
        self.assertIsNotNone(deps)
        self.assertEqual(len(deps), 4)
        self.assertIn("base-files", deps)
        self.assertIn("libc6", deps)
        self.assertIn("libtinfo6", deps)
        self.assertNotIn("libc6 (>= 2.34)", deps)

    def test_parse_package_no_dependencies(self):
        """Тест 2: Пакет без поля Depends."""
        self.set_up()
        deps = parse_package_dependencies(
            self.mock_packages_text, "no-deps-package", "1.0.0"
        )
        self.assertIsNotNone(deps)
        self.assertEqual(len(deps), 0)

    def test_parse_wrong_version(self):
        """Тест 3: Пакет есть, но версия не совпадает."""
        self.set_up()
        deps = parse_package_dependencies(
            self.mock_packages_text, "bash", "9.9.9-wrong"
        )
        self.assertIsNone(deps)

    def test_parse_non_existent_package(self):
        """Тест 4: Пакета нет в репозитории."""
        self.set_up()
        deps = parse_package_dependencies(
            self.mock_packages_text, "unknown-package", "1.0"
        )
        self.assertIsNone(deps)


if __name__ == '__main__':
    unittest.main()