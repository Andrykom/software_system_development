
def bucket_sort(arr, num_buckets=None):
    """Bucket sort с insertion sort для точного соответствия теории."""
    if not arr:
        return []
    
    if len(arr) == 1:
        return arr[:]
    
    if num_buckets is None:
        num_buckets = len(arr)
    
    min_val = min(arr)
    max_val = max(arr)
    
    if min_val == max_val:
        return arr[:]
    
    # Создаем ведра
    buckets = [[] for _ in range(num_buckets)]
    
    # Распределяем элементы
    for num in arr:
        # Стандартная формула
        if max_val == min_val:
            index = 0
        else:
            index = int((num - min_val) * num_buckets / (max_val - min_val + 1))
        
        if index >= num_buckets:
            index = num_buckets - 1
        
        buckets[index].append(num)
    
    # СОРТИРУЕМ КАЖДОЕ ВЕДРО INSERTION SORT (на Python)
    for bucket in buckets:
        real_insertion_sort(bucket)
    
    # Объединяем
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result


def real_insertion_sort(arr):
    """Настоящая сортировка вставками на Python для точных измерений."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # ВАЖНО: нет оптимизаций, чистый алгоритм
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
