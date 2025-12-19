"""
Unit-тесты для модуля bucket_sort.

Тесты проверяют корректность работы алгоритма Bucket Sort
в различных сценариях.
"""

import unittest
import sys
import os

# Добавляем родительскую директорию в путь для импорта модуля
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bucket_sort import bucket_sort, insertion_sort


class TestBucketSort(unittest.TestCase):
    """Класс для тестирования функции bucket_sort."""
    
    def test_empty_array(self):
        """Тест: сортировка пустого массива."""
        self.assertEqual(bucket_sort([]), [])
    
    def test_single_element(self):
        """Тест: сортировка массива с одним элементом."""
        self.assertEqual(bucket_sort([5]), [5])
    
    def test_sorted_array(self):
        """Тест: сортировка уже отсортированного массива."""
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(bucket_sort(arr), [1, 2, 3, 4, 5])
    
    def test_reverse_sorted_array(self):
        """Тест: сортировка массива, отсортированного в обратном порядке."""
        arr = [5, 4, 3, 2, 1]
        self.assertEqual(bucket_sort(arr), [1, 2, 3, 4, 5])
    
    def test_unsorted_array(self):
        """Тест: сортировка неотсортированного массива."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        self.assertEqual(bucket_sort(arr), [11, 12, 22, 25, 34, 64, 90])
    
    def test_duplicate_elements(self):
        """Тест: сортировка массива с повторяющимися элементами."""
        arr = [5, 2, 8, 2, 9, 1, 5, 5]
        self.assertEqual(bucket_sort(arr), [1, 2, 2, 5, 5, 5, 8, 9])
    
    def test_negative_numbers(self):
        """Тест: сортировка массива с отрицательными числами."""
        arr = [-5, 3, -1, 0, -3, 2]
        self.assertEqual(bucket_sort(arr), [-5, -3, -1, 0, 2, 3])
    
    def test_all_same_elements(self):
        """Тест: сортировка массива, где все элементы одинаковые."""
        arr = [5, 5, 5, 5, 5]
        self.assertEqual(bucket_sort(arr), [5, 5, 5, 5, 5])
    
    def test_large_array(self):
        """Тест: сортировка большого массива."""
        arr = list(range(100, 0, -1))
        expected = list(range(1, 101))
        self.assertEqual(bucket_sort(arr), expected)
    
    def test_custom_num_buckets(self):
        """Тест: сортировка с указанным количеством ведер."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = bucket_sort(arr, num_buckets=3)
        self.assertEqual(result, [11, 12, 22, 25, 34, 64, 90])
    
    def test_preserves_original_array(self):
        """Тест: проверка, что исходный массив не изменяется."""
        arr = [5, 2, 8, 1, 9]
        original = arr.copy()
        bucket_sort(arr)
        self.assertEqual(arr, original)
    
    def test_mixed_positive_negative(self):
        """Тест: сортировка массива со смешанными положительными и отрицательными числами."""
        arr = [10, -5, 0, 3, -10, 5, -3]
        self.assertEqual(bucket_sort(arr), [-10, -5, -3, 0, 3, 5, 10])


class TestInsertionSort(unittest.TestCase):
    """Класс для тестирования вспомогательной функции insertion_sort."""
    
    def test_insertion_sort_basic(self):
        """Тест: базовая проверка insertion_sort."""
        arr = [5, 2, 8, 1, 9]
        insertion_sort(arr)
        self.assertEqual(arr, [1, 2, 5, 8, 9])
    
    def test_insertion_sort_empty(self):
        """Тест: insertion_sort с пустым массивом."""
        arr = []
        insertion_sort(arr)
        self.assertEqual(arr, [])
    
    def test_insertion_sort_single(self):
        """Тест: insertion_sort с одним элементом."""
        arr = [5]
        insertion_sort(arr)
        self.assertEqual(arr, [5])


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
