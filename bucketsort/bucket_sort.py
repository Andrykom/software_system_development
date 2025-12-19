"""
Модуль для реализации алгоритма сортировки Bucket Sort (Блочная сортировка).

Bucket Sort - это алгоритм сортировки, который распределяет элементы массива
по "ведрам" (buckets), затем сортирует каждое ведро отдельно (обычно другим
алгоритмом сортировки), и наконец объединяет отсортированные ведра.
"""


def bucket_sort(arr, num_buckets=None):
    """
    Сортирует массив целых чисел с помощью алгоритма Bucket Sort.
    
    Args:
        arr: Список целых чисел для сортировки
        num_buckets: Количество ведер (по умолчанию равно длине массива)
    
    Returns:
        Отсортированный список целых чисел
    
    Временная сложность:
        Лучший случай: O(n) - когда элементы равномерно распределены
        Худший случай: O(n^2) - когда все элементы попадают в одно ведро
        Средний случай: O(n + k), где k - количество ведер
    """
    if not arr:
        return arr
    
    # Если массив содержит один элемент, он уже отсортирован
    if len(arr) == 1:
        return arr.copy()
    
    # Определяем количество ведер
    if num_buckets is None:
        num_buckets = len(arr)
    
    # Находим минимальное и максимальное значение
    min_val = min(arr)
    max_val = max(arr)
    
    # Если все элементы одинаковые, возвращаем копию массива
    if min_val == max_val:
        return arr.copy()
    
    # Вычисляем диапазон для каждого ведра
    bucket_range = (max_val - min_val) / num_buckets
    
    # Создаем ведра
    buckets = [[] for _ in range(num_buckets)]
    
    # Распределяем элементы по ведрам
    for num in arr:
        # Вычисляем индекс ведра
        bucket_index = int((num - min_val) / bucket_range)
        # Обрабатываем случай, когда элемент равен максимальному значению
        if bucket_index >= num_buckets:
            bucket_index = num_buckets - 1
        buckets[bucket_index].append(num)
    
    # Сортируем каждое ведро (используем insertion sort для простоты)
    for bucket in buckets:
        insertion_sort(bucket)
    
    # Объединяем отсортированные ведра
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(bucket)
    
    return sorted_arr


def insertion_sort(arr):
    """
    Вспомогательная функция для сортировки элементов внутри ведра.
    Использует алгоритм сортировки вставками.
    
    Args:
        arr: Список для сортировки
    
    Временная сложность: O(n^2) в худшем случае, O(n) в лучшем случае
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Перемещаем элементы, которые больше key, на одну позицию вперед
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
