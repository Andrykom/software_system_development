"""
Модуль для визуализации алгоритма Bucket Sort.

Генерирует пошаговые состояния для визуализации процесса сортировки.
"""


def bucket_sort_with_steps(arr, num_buckets=None, delay_callback=None):
    """
    Сортирует массив с генерацией шагов для визуализации.
    
    Args:
        arr: Список целых чисел для сортировки
        num_buckets: Количество ведер (по умолчанию равно длине массива)
        delay_callback: Функция обратного вызова для задержки между шагами
    
    Yields:
        Словарь с информацией о текущем состоянии сортировки:
        {
            'step': номер шага,
            'description': описание шага,
            'array': текущее состояние массива,
            'buckets': текущее состояние ведер,
            'current_bucket': индекс текущего ведра (если применимо),
            'comparing': индексы сравниваемых элементов (если применимо)
        }
    """
    if not arr:
        yield {
            'step': 0,
            'description': 'Массив пуст',
            'array': [],
            'buckets': [],
            'current_bucket': None,
            'comparing': None
        }
        return
    
    if len(arr) == 1:
        yield {
            'step': 0,
            'description': 'Массив содержит один элемент - уже отсортирован',
            'array': arr.copy(),
            'buckets': [],
            'current_bucket': None,
            'comparing': None
        }
        return
    
    step = 0
    
    # Определяем количество ведер
    if num_buckets is None:
        num_buckets = len(arr)
    
    # Находим минимальное и максимальное значение
    min_val = min(arr)
    max_val = max(arr)
    
    yield {
        'step': step,
        'description': f'Найдены min={min_val}, max={max_val}. Создано {num_buckets} ведер',
        'array': arr.copy(),
        'buckets': [[] for _ in range(num_buckets)],
        'current_bucket': None,
        'comparing': None
    }
    step += 1
    if delay_callback:
        delay_callback()
    
    # Если все элементы одинаковые
    if min_val == max_val:
        yield {
            'step': step,
            'description': 'Все элементы одинаковые - массив уже отсортирован',
            'array': arr.copy(),
            'buckets': [],
            'current_bucket': None,
            'comparing': None
        }
        return
    
    # Вычисляем диапазон для каждого ведра
    bucket_range = (max_val - min_val) / num_buckets
    
    # Создаем ведра
    buckets = [[] for _ in range(num_buckets)]
    
    # Распределяем элементы по ведрам
    for i, num in enumerate(arr):
        bucket_index = int((num - min_val) / bucket_range)
        if bucket_index >= num_buckets:
            bucket_index = num_buckets - 1
        buckets[bucket_index].append(num)
        
        yield {
            'step': step,
            'description': f'Элемент {num} помещен в ведро {bucket_index}',
            'array': arr.copy(),
            'buckets': [bucket.copy() for bucket in buckets],
            'current_bucket': bucket_index,
            'comparing': i
        }
        step += 1
        if delay_callback:
            delay_callback()
    
    yield {
        'step': step,
        'description': 'Распределение элементов по ведрам завершено',
        'array': arr.copy(),
        'buckets': [bucket.copy() for bucket in buckets],
        'current_bucket': None,
        'comparing': None
    }
    step += 1
    if delay_callback:
        delay_callback()
    
    # Сортируем каждое ведро
    for bucket_idx, bucket in enumerate(buckets):
        if len(bucket) > 1:
            yield {
                'step': step,
                'description': f'Начало сортировки ведра {bucket_idx}',
                'array': arr.copy(),
                'buckets': [bucket.copy() for bucket in buckets],
                'current_bucket': bucket_idx,
                'comparing': None
            }
            step += 1
            if delay_callback:
                delay_callback()
            
            # Insertion sort с шагами
            for i in range(1, len(bucket)):
                key = bucket[i]
                j = i - 1
                
                yield {
                    'step': step,
                    'description': f'Сортировка ведра {bucket_idx}: сравнение элементов',
                    'array': arr.copy(),
                    'buckets': [bucket.copy() for bucket in buckets],
                    'current_bucket': bucket_idx,
                    'comparing': (j, i)
                }
                step += 1
                if delay_callback:
                    delay_callback()
                
                while j >= 0 and bucket[j] > key:
                    bucket[j + 1] = bucket[j]
                    j -= 1
                    
                    yield {
                        'step': step,
                        'description': f'Сортировка ведра {bucket_idx}: перемещение элементов',
                        'array': arr.copy(),
                        'buckets': [bucket.copy() for bucket in buckets],
                        'current_bucket': bucket_idx,
                        'comparing': (j + 1, j)
                    }
                    step += 1
                    if delay_callback:
                        delay_callback()
                
                bucket[j + 1] = key
                
                yield {
                    'step': step,
                    'description': f'Сортировка ведра {bucket_idx}: элемент {key} вставлен',
                    'array': arr.copy(),
                    'buckets': [bucket.copy() for bucket in buckets],
                    'current_bucket': bucket_idx,
                    'comparing': (j + 1,)
                }
                step += 1
                if delay_callback:
                    delay_callback()
            
            yield {
                'step': step,
                'description': f'Ведро {bucket_idx} отсортировано',
                'array': arr.copy(),
                'buckets': [bucket.copy() for bucket in buckets],
                'current_bucket': bucket_idx,
                'comparing': None
            }
            step += 1
            if delay_callback:
                delay_callback()
    
    # Объединяем отсортированные ведра
    sorted_arr = []
    for bucket_idx, bucket in enumerate(buckets):
        sorted_arr.extend(bucket)
        
        yield {
            'step': step,
            'description': f'Ведро {bucket_idx} объединено с результатом',
            'array': sorted_arr.copy(),
            'buckets': [bucket.copy() for bucket in buckets],
            'current_bucket': bucket_idx,
            'comparing': None
        }
        step += 1
        if delay_callback:
            delay_callback()
    
    yield {
        'step': step,
        'description': 'Сортировка завершена!',
        'array': sorted_arr,
        'buckets': [bucket.copy() for bucket in buckets],
        'current_bucket': None,
        'comparing': None
    }
