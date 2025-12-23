"""
Модуль для работы с базой данных SQLite.

Реализует хранение пользователей и истории сортировок.
"""

import sqlite3
import hashlib
import json
from typing import Optional, List, Tuple, Dict


class Database:
    """Класс для работы с базой данных SQLite."""
    
    def __init__(self, db_path: str = "bucketsort.db"):
        """
        Инициализирует подключение к базе данных.
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Создает и возвращает подключение к базе данных."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Инициализирует структуру базы данных."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Таблица истории сортировок
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sort_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                original_array TEXT NOT NULL,
                sorted_array TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # Индекс для быстрого поиска по user_id
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sort_history_user_id 
            ON sort_history(user_id)
        """)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """
        Хеширует пароль с использованием SHA-256.
        
        Args:
            password: Пароль в открытом виде
            
        Returns:
            Хеш пароля
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Регистрирует нового пользователя.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            Кортеж (успех, сообщение)
        """
        if not username or not password:
            return False, "Имя пользователя и пароль не могут быть пустыми"
        
        if len(username) < 3:
            return False, "Имя пользователя должно содержать минимум 3 символа"
        
        if len(password) < 4:
            return False, "Пароль должен содержать минимум 4 символа"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            return True, "Пользователь успешно зарегистрирован"
        except sqlite3.IntegrityError:
            return False, "Пользователь с таким именем уже существует"
        except Exception as e:
            return False, f"Ошибка при регистрации: {str(e)}"
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[int]:
        """
        Аутентифицирует пользователя.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            ID пользователя при успешной аутентификации, None в противном случае
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        return result['id'] if result else None
    
    def save_sort_history(self, user_id: int, original_array: List[int], sorted_array: List[int]) -> Tuple[bool, str]:
        """
        Сохраняет историю сортировки для пользователя.
        
        Args:
            user_id: ID пользователя
            original_array: Исходный массив
            sorted_array: Отсортированный массив
            
        Returns:
            Кортеж (успех, сообщение)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Сохраняем массивы как JSON строки
            original_json = json.dumps(original_array)
            sorted_json = json.dumps(sorted_array)
            
            cursor.execute(
                """INSERT INTO sort_history (user_id, original_array, sorted_array) 
                   VALUES (?, ?, ?)""",
                (user_id, original_json, sorted_json)
            )
            conn.commit()
            return True, "История сохранена"
        except Exception as e:
            return False, f"Ошибка при сохранении: {str(e)}"
        finally:
            conn.close()
    
    def get_sort_history(self, user_id: int, limit: int = 100) -> List[Dict]:
        """
        Получает историю сортировок пользователя.
        
        Args:
            user_id: ID пользователя
            limit: Максимальное количество записей
            
        Returns:
            Список словарей с историей сортировок
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, original_array, sorted_array, created_at
            FROM sort_history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'original_array': json.loads(row['original_array']),
                'sorted_array': json.loads(row['sorted_array']),
                'created_at': row['created_at']
            })
        
        conn.close()
        return results
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Получает информацию о пользователе по ID.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Словарь с информацией о пользователе или None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'username': row['username'],
                'created_at': row['created_at']
            }
        return None
    
    def clear_all_history(self) -> Tuple[bool, str]:
        """
        Очищает всю историю сортировок (для тестов).
        
        Returns:
            Кортеж (успех, сообщение)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM sort_history")
            conn.commit()
            return True, "История очищена"
        except Exception as e:
            return False, f"Ошибка при очистке: {str(e)}"
        finally:
            conn.close()
    
    def get_all_arrays(self, limit: int = None) -> List[Dict]:
        """
        Получает все массивы из базы данных (для тестов).
        
        Args:
            limit: Максимальное количество записей
            
        Returns:
            Список словарей с массивами
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if limit:
            cursor.execute("""
                SELECT original_array, sorted_array
                FROM sort_history
                LIMIT ?
            """, (limit,))
        else:
            cursor.execute("""
                SELECT original_array, sorted_array
                FROM sort_history
            """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'original_array': json.loads(row['original_array']),
                'sorted_array': json.loads(row['sorted_array'])
            })
        
        conn.close()
        return results

