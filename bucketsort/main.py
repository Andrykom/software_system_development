"""
Консольное приложение для сортировки массивов с помощью алгоритма Bucket Sort.

Приложение предоставляет следующие возможности:
- Ввод массива с клавиатуры
- Генерация случайного массива
- Загрузка массива из файла
- Сортировка массива
- Вывод результатов
- Сохранение результатов в файл
"""

import random
import os
from bucket_sort import bucket_sort


def print_menu():
    """Выводит главное меню приложения."""
    print("\n" + "="*50)
    print("КОНСОЛЬНОЕ ПРИЛОЖЕНИЕ ДЛЯ СОРТИРОВКИ BUCKET SORT")
    print("="*50)
    print("1. Ввести массив с клавиатуры")
    print("2. Сгенерировать случайный массив")
    print("3. Загрузить массив из файла")
    print("4. Отсортировать массив")
    print("5. Вывести массивы на экран")
    print("6. Сохранить массивы в файл")
    print("0. Выход")
    print("="*50)


def input_array_from_keyboard():
    """
    Запрашивает у пользователя ввод массива с клавиатуры.
    
    Returns:
        Список целых чисел или None в случае ошибки
    """
    try:
        print("\nВведите элементы массива через пробел:")
        input_str = input().strip()
        if not input_str:
            print("Ошибка: массив не может быть пустым!")
            return None
        
        arr = [int(x) for x in input_str.split()]
        print(f"Введен массив: {arr}")
        return arr
    except ValueError:
        print("Ошибка: введите только целые числа, разделенные пробелами!")
        return None
    except Exception as e:
        print(f"Ошибка при вводе: {e}")
        return None


def generate_random_array():
    """
    Генерирует случайный массив целых чисел.
    
    Returns:
        Список случайных целых чисел
    """
    try:
        print("\nГенерация случайного массива")
        size = int(input("Введите размер массива: "))
        if size <= 0:
            print("Ошибка: размер должен быть положительным числом!")
            return None
        
        min_val = int(input("Введите минимальное значение: "))
        max_val = int(input("Введите максимальное значение: "))
        
        if min_val > max_val:
            print("Ошибка: минимальное значение не может быть больше максимального!")
            return None
        
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        print(f"Сгенерирован массив: {arr}")
        return arr
    except ValueError:
        print("Ошибка: введите целые числа!")
        return None
    except Exception as e:
        print(f"Ошибка при генерации: {e}")
        return None


def load_array_from_file():
    """
    Загружает массив из файла.
    
    Returns:
        Список целых чисел или None в случае ошибки
    """
    try:
        filename = input("\nВведите имя файла: ").strip()
        if not filename:
            print("Ошибка: имя файла не может быть пустым!")
            return None
        
        if not os.path.exists(filename):
            print(f"Ошибка: файл '{filename}' не найден!")
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print("Ошибка: файл пуст!")
                return None
            
            # Пытаемся прочитать числа, разделенные пробелами или переносами строк
            numbers = []
            for line in content.split('\n'):
                numbers.extend([int(x) for x in line.split() if x.strip()])
            
            if not numbers:
                print("Ошибка: в файле не найдено целых чисел!")
                return None
            
            print(f"Загружен массив из файла '{filename}': {numbers}")
            return numbers
    except ValueError:
        print("Ошибка: файл должен содержать только целые числа!")
        return None
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}' не найден!")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None


def save_arrays_to_file(original_arr, sorted_arr):
    """
    Сохраняет исходный и отсортированный массивы в файл.
    
    Args:
        original_arr: Исходный массив
        sorted_arr: Отсортированный массив
    """
    try:
        filename = input("\nВведите имя файла для сохранения: ").strip()
        if not filename:
            print("Ошибка: имя файла не может быть пустым!")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Исходный массив:\n")
            f.write(' '.join(map(str, original_arr)) + '\n\n')
            f.write("Отсортированный массив:\n")
            f.write(' '.join(map(str, sorted_arr)) + '\n')
        
        print(f"Массивы успешно сохранены в файл '{filename}'")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


def print_arrays(original_arr, sorted_arr):
    """
    Выводит исходный и отсортированный массивы на экран.
    
    Args:
        original_arr: Исходный массив
        sorted_arr: Отсортированный массив
    """
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ СОРТИРОВКИ")
    print("="*50)
    print(f"Исходный массив:     {original_arr}")
    print(f"Отсортированный массив: {sorted_arr}")
    print("="*50)


def main():
    """Главная функция приложения."""
    original_array = None
    sorted_array = None
    
    while True:
        print_menu()
        choice = input("Выберите пункт меню: ").strip()
        
        if choice == '0':
            print("\nДо свидания!")
            break
        
        elif choice == '1':
            original_array = input_array_from_keyboard()
            sorted_array = None
        
        elif choice == '2':
            original_array = generate_random_array()
            sorted_array = None
        
        elif choice == '3':
            original_array = load_array_from_file()
            sorted_array = None
        
        elif choice == '4':
            if original_array is None:
                print("\nОшибка: сначала загрузите или введите массив!")
            else:
                print("\nВыполняется сортировка...")
                sorted_array = bucket_sort(original_array.copy())
                print("Сортировка завершена!")
                print_arrays(original_array, sorted_array)
        
        elif choice == '5':
            if original_array is None:
                print("\nОшибка: массив не загружен!")
            elif sorted_array is None:
                print("\nОшибка: массив не отсортирован! Сначала выполните сортировку.")
            else:
                print_arrays(original_array, sorted_array)
        
        elif choice == '6':
            if original_array is None:
                print("\nОшибка: массив не загружен!")
            elif sorted_array is None:
                print("\nОшибка: массив не отсортирован! Сначала выполните сортировку.")
            else:
                save_arrays_to_file(original_array, sorted_array)
        
        else:
            print("\nОшибка: неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
