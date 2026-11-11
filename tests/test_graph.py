import unittest
import os
import tempfile
from src.graph import (
    parse_test_graph,
    build_dependency_graph,
    build_reverse_graph,
    get_reverse_dependencies
)


class TestGraphLogic(unittest.TestCase):

    def setUp(self):  # noqa: N802
        """Подготовка тестовых данных."""
        self.test_graph_data = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': ['A'],
            'E': ['F'],
            'F': []
        }

    def test_build_dependency_graph_test_mode(self):
        """Тест построения графа в тестовом режиме."""
        graph = build_dependency_graph(
            'A', None, is_test_mode=True, test_graph=self.test_graph_data
        )
        
        self.assertIn('A', graph)
        self.assertIn('B', graph)
        self.assertIn('D', graph)
        self.assertEqual(graph['A'], ['B', 'C'])
        self.assertEqual(graph['B'], ['D'])

    def test_build_reverse_graph(self):
        """Тест построения обратного графа."""
        reverse_graph = build_reverse_graph(self.test_graph_data)
        
        self.assertIn('D', reverse_graph)
        self.assertIn('B', reverse_graph['D'])
        self.assertIn('C', reverse_graph['D'])
        
        self.assertIn('A', reverse_graph)
        self.assertIn('D', reverse_graph['A'])

    def test_get_reverse_dependencies_transitive(self):
        """Тест поиска транзитивных обратных зависимостей."""
        reverse_deps = get_reverse_dependencies(
            'D', self.test_graph_data, is_test_mode=True
        )
        
        self.assertIn('B', reverse_deps)
        self.assertIn('C', reverse_deps)
        self.assertIn('A', reverse_deps)

    def test_get_reverse_dependencies_no_deps(self):
        """Тест поиска обратных зависимостей без вложенности."""
        reverse_deps = get_reverse_dependencies(
            'F', self.test_graph_data, is_test_mode=True
        )
        
        self.assertIn('E', reverse_deps)
        self.assertNotIn('A', reverse_deps)

    def test_get_reverse_dependencies_isolated(self):
        """Тест поиска для изолированного пакета."""
        reverse_deps = get_reverse_dependencies(
            'Z', self.test_graph_data, is_test_mode=True
        )
        
        self.assertEqual(reverse_deps, [])

    def test_parse_test_graph_file(self):
        """Тест парсинга файла тестового графа."""
        with tempfile.NamedTemporaryFile(
            mode='w', delete=False, encoding='utf-8'
        ) as f:
            f.write("X: Y, Z\n")
            f.write("Y: Z\n")
            f.write("Z:\n")
            temp_path = f.name
            
        try:
            graph = parse_test_graph(temp_path)
            self.assertEqual(graph['X'], ['Y', 'Z'])
            self.assertEqual(graph['Y'], ['Z'])
            self.assertEqual(graph['Z'], [])
        finally:
            os.remove(temp_path)


if __name__ == '__main__':
    unittest.main()