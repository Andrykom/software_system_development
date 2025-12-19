"""
Тесты для оценки временной сложности Bucket Sort в лучшем и худшем случаях.
"""

import unittest
import sys
import os
import time
import random

# Добавляем родительскую директорию в путь для импорта модуля
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bucket_sort import bucket_sort


class TestBucketSortComplexity(unittest.TestCase):
    """Тесты для оценки временной сложности Bucket Sort."""
    
    def test_best_case_complexity(self):
        """
        Тест лучшего случая: элементы равномерно распределены по ведрам.
        В идеале - в каждом ведре по 1 элементу.
        Ожидаемая сложность: O(n)
        """
        print("\n" + "="*60)
        print("Тест ЛУЧШЕГО случая (равномерное распределение)")
        print("Ожидаемая сложность: O(n)")
        print("="*60)
        
        sizes = [1000, 5000, 10000, 20000, 50000]
        results = []
        
        for size in sizes:
            # Создаем равномерно распределенные данные
            # Диапазон значительно больше размера массива
            min_val = 0
            max_val = size * 100  # Большой диапазон для равномерного распределения
            arr = [random.randint(min_val, max_val) for _ in range(size)]
            
            start_time = time.perf_counter()
            result = bucket_sort(arr)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            results.append((size, execution_time))
            
            # Проверяем корректность сортировки
            self.assertEqual(result, sorted(arr))
            
            print(f"Размер: {size:6d} | Время: {execution_time:.6f} сек")
        
        # Анализ роста времени
        print("\nАнализ роста времени (для O(n) время должно расти линейно):")
        for i in range(1, len(results)):
            size_ratio = results[i][0] / results[0][0]
            time_ratio = results[i][1] / results[0][1]
            print(f"Увеличение размера в {size_ratio:5.1f} раз -> время увеличилось в {time_ratio:5.1f} раз")
    
    def test_worst_case_complexity(self):
        """
        Тест худшего случая: все элементы попадают в одно ведро.
        Для этого создаем данные с очень маленьким диапазоном
        при большом количестве ведер.
        Ожидаемая сложность: O(n²)
        """
        print("\n" + "="*60)
        print("Тест ХУДШЕГО случая (все элементы в одном ведре)")
        print("Ожидаемая сложность: O(n²)")
        print("="*60)
        
        # Используем меньшее количество элементов из-за квадратичной сложности
        sizes = [100, 200, 400, 800, 1600]
        results = []
        
        for size in sizes:
            # Создаем данные с очень маленьким диапазоном
            # Все элементы будут в одном или двух ведрах
            arr = [random.randint(1, 10) for _ in range(size)]  # Диапазон всего 10 значений
            
            # Используем много ведер (по умолчанию size), чтобы все элементы 
            # с высокой вероятностью попали в одно ведро
            start_time = time.perf_counter()
            result = bucket_sort(arr)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            results.append((size, execution_time))
            
            # Проверяем корректность сортировки
            self.assertEqual(result, sorted(arr))
            
            print(f"Размер: {size:6d} | Время: {execution_time:.6f} сек")
        
        # Анализ роста времени
        print("\nАнализ роста времени (для O(n²) время должно расти квадратично):")
        for i in range(1, len(results)):
            size_ratio = results[i][0] / results[0][0]
            time_ratio = results[i][1] / results[0][1]
            expected_quadratic = size_ratio ** 2
            print(f"Увеличение размера в {size_ratio:5.1f} раз -> "
                  f"время увеличилось в {time_ratio:5.1f} раз "
                  f"(ожидалось: {expected_quadratic:5.1f})")
    
    def test_all_elements_same(self):
        """
        Тест: все элементы одинаковые.
        В вашей реализации это оптимизированный случай O(n).
        """
        print("\n" + "="*60)
        print("Тест: все элементы одинаковые (оптимизированный случай)")
        print("Ожидаемая сложность: O(n) благодаря оптимизации")
        print("="*60)
        
        sizes = [1000, 5000, 10000, 50000, 100000]
        results = []
        
        for size in sizes:
            arr = [42] * size  # Все элементы одинаковые
            
            start_time = time.perf_counter()
            result = bucket_sort(arr)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            results.append((size, execution_time))
            
            # Проверяем корректность
            self.assertEqual(result, arr)
            
            print(f"Размер: {size:6d} | Время: {execution_time:.6f} сек")
        
        # Анализ роста времени
        print("\nАнализ роста времени:")
        for i in range(1, len(results)):
            size_ratio = results[i][0] / results[0][0]
            time_ratio = results[i][1] / results[0][1]
            print(f"Увеличение размера в {size_ratio:5.1f} раз -> время увеличилось в {time_ratio:5.1f} раз")
    
    def test_single_bucket_worst_case(self):
        """
        Тест: насильно заставляем все элементы попасть в одно ведро.
        Используем num_buckets=1.
        """
        print("\n" + "="*60)
        print("Тест: все элементы в ОДНОМ ведре (num_buckets=1)")
        print("Ожидаемая сложность: O(n²) - insertion sort всего массива")
        print("="*60)
        
        sizes = [100, 200, 400, 800, 1600]
        results = []
        
        for size in sizes:
            arr = list(range(size, 0, -1))  # Обратно отсортированный массив
            
            start_time = time.perf_counter()
            result = bucket_sort(arr, num_buckets=1)  # Только одно ведро!
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            results.append((size, execution_time))
            
            # Проверяем корректность
            self.assertEqual(result, sorted(arr))
            
            print(f"Размер: {size:6d} | Время: {execution_time:.6f} сек")
        
        # Анализ квадратичного роста
        print("\nКвадратичный анализ (n² vs фактическое время):")
        for size, time_taken in results:
            # Нормализуем относительно 100 элементов
            if size == 100:
                base_time = time_taken
                base_size = size
                print(f"Базовый размер {base_size}: время = {base_time:.6f}, n² = {base_size**2}")
            else:
                expected_ratio = (size**2) / (base_size**2)
                actual_ratio = time_taken / base_time
                print(f"Размер {size:5d}: время = {time_taken:.6f}, "
                      f"n² отношение = {expected_ratio:7.1f}, "
                      f"фактическое отношение = {actual_ratio:7.1f}")
    
    def test_linear_growth_ideal_case(self):
        """
        Тест: идеальный случай - в каждом ведре ровно 1 элемент.
        Достигается созданием size уникальных значений от 0 до size-1.
        """
        print("\n" + "="*60)
        print("Тест: идеальный случай (по 1 элементу в каждом ведре)")
        print("Ожидаемая сложность: O(n)")
        print("="*60)
        
        sizes = [1000, 2000, 4000, 8000, 16000, 32000]
        results = []
        
        for size in sizes:
            # Создаем size уникальных значений от 0 до size-1
            arr = list(range(size))
            random.shuffle(arr)  # Перемешиваем
            
            start_time = time.perf_counter()
            result = bucket_sort(arr)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            results.append((size, execution_time))
            
            # Проверяем корректность
            self.assertEqual(result, list(range(size)))
            
            print(f"Размер: {size:6d} | Время: {execution_time:.6f} сек")
        
        # Анализ линейного роста
        print("\nЛинейный анализ (n vs фактическое время):")
        for i in range(1, len(results)):
            size_ratio = results[i][0] / results[i-1][0]
            time_ratio = results[i][1] / results[i-1][1]
            print(f"Размер увеличился в {size_ratio:4.1f} раз -> "
                  f"время увеличилось в {time_ratio:4.1f} раз")
    
    def test_comparison_with_quadratic(self):
        """
        Сравнение времени работы с ожидаемой квадратичной сложностью.
        """
        print("\n" + "="*60)
        print("Сравнение с теоретической квадратичной сложностью")
        print("="*60)
        
        sizes = [50, 100, 200, 400, 800]
        
        print("\nАнализ для худшего случая (num_buckets=1):")
        print("Размер | Время (сек) | Отношение к предыдущему | Ожидаемое (n²)")
        print("-" * 65)
        
        prev_time = None
        prev_size = None
        
        for size in sizes:
            arr = list(range(size, 0, -1))
            
            start_time = time.perf_counter()
            result = bucket_sort(arr, num_buckets=1)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            
            if prev_time is not None:
                size_ratio = size / prev_size
                time_ratio = execution_time / prev_time
                expected_ratio = size_ratio ** 2
                print(f"{size:6d} | {execution_time:11.6f} | {time_ratio:21.2f} | {expected_ratio:13.2f}")
            else:
                print(f"{size:6d} | {execution_time:11.6f} | {'-':21} | {'-':13}")
            
            prev_time = execution_time
            prev_size = size
            self.assertEqual(result, sorted(arr))
    
    def test_bucket_distribution_effect(self):
        """
        Тест влияния распределения по ведрам на производительность.
        """
        print("\n" + "="*60)
        print("Влияние распределения по ведрам на производительность")
        print("="*60)
        
        size = 5000
        test_cases = [
            ("Очень плохое", 1, 10),        # Все в 1-2 ведрах
            ("Плохое", 1, 100),             # В нескольких ведрах
            ("Среднее", 1, 1000),           # Умеренное распределение
            ("Хорошее", 1, 10000),          # Хорошее распределение
            ("Отличное", 1, 100000),        # Отличное распределение
            ("Идеальное", 0, size-1),       # Уникальные значения
        ]
        
        print(f"\nРазмер массива: {size}")
        print(f"{'Распределение':<15} | {'Диапазон':<12} | {'Время (сек)':<12}")
        print("-" * 50)
        
        for name, min_range, max_range in test_cases:
            if name == "Идеальное":
                arr = list(range(size))
                random.shuffle(arr)
            else:
                arr = [random.randint(min_range, max_range) for _ in range(size)]
            
            start_time = time.perf_counter()
            result = bucket_sort(arr)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            
            print(f"{name:<15} | {f'{min_range}-{max_range}':<12} | {execution_time:<12.6f}")
            
            # Проверяем корректность
            self.assertEqual(result, sorted(arr))


def calculate_complexity_coefficient(sizes, times):
    """
    Вычисляет коэффициент временной сложности на основе данных.
    """
    if len(sizes) < 2:
        return None
    
    # Логарифмируем данные для линейной регрессии
    import math
    log_sizes = [math.log(s) for s in sizes]
    log_times = [math.log(t) for t in times]
    
    # Вычисляем наклон (коэффициент сложности)
    n = len(sizes)
    sum_xy = sum(log_sizes[i] * log_times[i] for i in range(n))
    sum_x = sum(log_sizes)
    sum_y = sum(log_times)
    sum_x2 = sum(x*x for x in log_sizes)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    
    return slope


if __name__ == '__main__':
    print("\n" + "="*60)
    print("ТЕСТИРОВАНИЕ ВРЕМЕННОЙ СЛОЖНОСТИ BUCKET SORT")
    print("="*60)
    
    # Создаем тестовый набор
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBucketSortComplexity)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
    print("\n" + "="*60)
    print("РЕЗЮМЕ:")
    print("="*60)
    print("1. Лучший случай (равномерное распределение): O(n)")
    print("2. Худший случай (все в одном ведре): O(n²)")
    print("3. Все элементы одинаковые: O(n) (благодаря оптимизации)")
    print("4. Средний случай: O(n + n²/k), где k - количество ведер")
    print("="*60)
