"""
Интеграционные тесты для работы с базой данных.

Тесты проверяют производительность операций с базой данных:
- Добавление массивов
- Выгрузка и сортировка массивов
- Очистка базы данных
"""

import sys
import os
import time
import random
import json

# Добавляем путь к модулям проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bucketsort.database import Database
from bucketsort.bucket_sort import bucket_sort


class DatabaseIntegrationTests:
    """Класс для интеграционных тестов базы данных."""
    
    def __init__(self, db_path: str = "test_bucketsort.db"):
        """
        Инициализирует тесты.
        
        Args:
            db_path: Путь к тестовой базе данных
        """
        self.db = Database(db_path)
        self.db_path = db_path
    
    def generate_random_array(self, size: int, min_val: int = 1, max_val: int = 1000) -> list:
        """
        Генерирует случайный массив целых чисел.
        
        Args:
            size: Размер массива
            min_val: Минимальное значение
            max_val: Максимальное значение
            
        Returns:
            Список случайных целых чисел
        """
        return [random.randint(min_val, max_val) for _ in range(size)]
    
    def test_add_arrays(self, count: int) -> tuple:
        """
        Тест добавления массивов в базу данных.
        
        Args:
            count: Количество массивов для добавления
            
        Returns:
            Кортеж (успех, время работы в секундах)
        """
        start_time = time.time()
        success_count = 0
        
        try:
            # Получаем или создаем тестового пользователя
            user_id = self.db.authenticate_user("test_user", "testpass")
            if not user_id:
                # Создаем нового пользователя
                success, msg = self.db.register_user("test_user", "testpass")
                if not success:
                    return False, 0.0
                user_id = self.db.authenticate_user("test_user", "testpass")
                if not user_id:
                    return False, 0.0
            
            # Добавляем массивы
            for i in range(count):
                # Генерируем случайный массив
                array_size = random.randint(10, 100)
                original_array = self.generate_random_array(array_size)
                sorted_array = bucket_sort(original_array.copy())
                
                # Сохраняем в базу
                success, msg = self.db.save_sort_history(user_id, original_array, sorted_array)
                if success:
                    success_count += 1
            
            elapsed_time = time.time() - start_time
            return success_count == count, elapsed_time
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"Ошибка при добавлении массивов: {e}")
            return False, elapsed_time
    
    def test_load_and_sort_arrays(self, count: int, db_size: int) -> tuple:
        """
        Тест выгрузки и сортировки массивов из базы данных.
        
        Args:
            count: Количество массивов для обработки
            db_size: Размер базы данных (для информации)
            
        Returns:
            Кортеж (успех, общее время, среднее время на массив)
        """
        start_time = time.time()
        success_count = 0
        total_sort_time = 0.0
        
        try:
            # Получаем пользователя
            user_id = self.db.authenticate_user("test_user", "testpass")
            if not user_id:
                return False, 0.0, 0.0
            
            # Получаем массивы из базы
            arrays = self.db.get_sort_history(user_id, limit=count)
            
            if len(arrays) < count:
                print(f"Предупреждение: в базе только {len(arrays)} записей, запрошено {count}")
                count = len(arrays)
            
            if count == 0:
                return False, 0.0, 0.0
            
            # Обрабатываем каждый массив
            for i in range(min(count, len(arrays))):
                try:
                    original_array = arrays[i]['original_array']
                    
                    # Сортируем массив
                    sort_start = time.time()
                    sorted_result = bucket_sort(original_array.copy())
                    sort_time = time.time() - sort_start
                    
                    total_sort_time += sort_time
                    success_count += 1
                    
                except Exception as e:
                    print(f"Ошибка при обработке массива {i}: {e}")
            
            elapsed_time = time.time() - start_time
            avg_time = total_sort_time / success_count if success_count > 0 else 0.0
            
            return success_count == count, elapsed_time, avg_time
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"Ошибка при выгрузке и сортировке: {e}")
            return False, elapsed_time, 0.0
    
    def test_clear_database(self) -> tuple:
        """
        Тест очистки базы данных.
        
        Returns:
            Кортеж (успех, время работы в секундах)
        """
        start_time = time.time()
        
        try:
            success, msg = self.db.clear_all_history()
            elapsed_time = time.time() - start_time
            return success, elapsed_time
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"Ошибка при очистке базы данных: {e}")
            return False, elapsed_time
    
    def prepare_database(self, size: int):
        """
        Подготавливает базу данных заданного размера.
        
        Args:
            size: Количество записей в базе данных
        """
        print(f"Подготовка базы данных с {size} записями...")
        success, elapsed = self.test_add_arrays(size)
        if success:
            print(f"База данных подготовлена: {size} записей за {elapsed:.2f} секунд")
        else:
            print(f"Ошибка при подготовке базы данных")
    
    def cleanup(self):
        """Очищает тестовую базу данных."""
        try:
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                print(f"Тестовая база данных {self.db_path} удалена")
        except Exception as e:
            print(f"Ошибка при удалении тестовой базы данных: {e}")


def run_tests():
    """Запускает все интеграционные тесты."""
    print("=" * 70)
    print("ИНТЕГРАЦИОННЫЕ ТЕСТЫ БАЗЫ ДАННЫХ")
    print("=" * 70)
    print()
    
    tester = DatabaseIntegrationTests("test_bucketsort.db")
    
    # Тест 1: Добавление массивов
    print("ТЕСТ 1: Добавление массивов в базу данных")
    print("-" * 70)
    
    for count in [100, 1000, 10000]:
        print(f"\nДобавление {count} массивов...")
        success, elapsed = tester.test_add_arrays(count)
        status = "✓ УСПЕШНО" if success else "✗ ОШИБКА"
        print(f"Результат: {status}")
        print(f"Время работы: {elapsed:.2f} секунд")
        print(f"Скорость: {count/elapsed:.2f} массивов/сек" if elapsed > 0 else "N/A")
    
    print("\n" + "=" * 70)
    
    # Тест 2: Выгрузка и сортировка массивов
    print("\nТЕСТ 2: Выгрузка и сортировка 100 случайных массивов")
    print("-" * 70)
    
    for db_size in [100, 1000, 10000]:
        print(f"\nТест для базы данных с {db_size} записями:")
        
        # Подготавливаем базу данных
        tester.cleanup()
        tester = DatabaseIntegrationTests("test_bucketsort.db")
        tester.prepare_database(db_size)
        
        # Выполняем тест
        success, total_time, avg_time = tester.test_load_and_sort_arrays(100, db_size)
        status = "✓ УСПЕШНО" if success else "✗ ОШИБКА"
        print(f"Результат: {status}")
        print(f"Общее время работы: {total_time:.4f} секунд")
        print(f"Среднее время работы с 1 массивом: {avg_time:.6f} секунд")
    
    print("\n" + "=" * 70)
    
    # Тест 3: Очистка базы данных
    print("\nТЕСТ 3: Очистка базы данных")
    print("-" * 70)
    
    for db_size in [100, 1000, 10000]:
        print(f"\nТест очистки для базы данных с {db_size} записями:")
        
        # Подготавливаем базу данных
        tester.cleanup()
        tester = DatabaseIntegrationTests("test_bucketsort.db")
        tester.prepare_database(db_size)
        
        # Выполняем тест очистки
        success, elapsed = tester.test_clear_database()
        status = "✓ УСПЕШНО" if success else "✗ ОШИБКА"
        print(f"Результат: {status}")
        print(f"Время работы: {elapsed:.4f} секунд")
    
    print("\n" + "=" * 70)
    print("\nВсе тесты завершены!")
    
    # Очистка
    tester.cleanup()


if __name__ == "__main__":
    run_tests()

