"""
Модуль для работы с аутентификацией пользователей.
"""

from database import Database
from typing import Optional, Tuple


class AuthManager:
    """Менеджер аутентификации пользователей."""
    
    def __init__(self, db_path: str = "bucketsort.db"):
        """
        Инициализирует менеджер аутентификации.
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db = Database(db_path)
        self.current_user_id: Optional[int] = None
        self.current_username: Optional[str] = None
    
    def register(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Регистрирует нового пользователя.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            Кортеж (успех, сообщение)
        """
        return self.db.register_user(username, password)
    
    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Выполняет вход пользователя.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            Кортеж (успех, сообщение)
        """
        user_id = self.db.authenticate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            self.current_username = username
            return True, f"Добро пожаловать, {username}!"
        else:
            return False, "Неверное имя пользователя или пароль"
    
    def logout(self):
        """Выполняет выход пользователя."""
        self.current_user_id = None
        self.current_username = None
    
    def is_authenticated(self) -> bool:
        """
        Проверяет, аутентифицирован ли текущий пользователь.
        
        Returns:
            True если пользователь аутентифицирован, False в противном случае
        """
        return self.current_user_id is not None
    
    def get_current_user_id(self) -> Optional[int]:
        """
        Возвращает ID текущего пользователя.
        
        Returns:
            ID пользователя или None
        """
        return self.current_user_id
    
    def get_current_username(self) -> Optional[str]:
        """
        Возвращает имя текущего пользователя.
        
        Returns:
            Имя пользователя или None
        """
        return self.current_username

