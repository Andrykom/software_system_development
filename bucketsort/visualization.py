"""
GUI приложение для визуализации алгоритма Bucket Sort.

Использует Tkinter для создания графического интерфейса с анимацией процесса сортировки.
Включает систему авторизации и сохранение истории сортировок в базе данных.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import threading
import time
from bucket_sort_visualizer import bucket_sort_with_steps
from bucket_sort import bucket_sort
from auth import AuthManager


class BucketSortVisualizer:
    """Класс для визуализации алгоритма Bucket Sort."""
    
    MAX_ARRAY_SIZE = 100  # Максимальный размер массива для визуализации
    
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация Bucket Sort")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f0f0f0')
        
        # Менеджер аутентификации
        self.auth_manager = AuthManager()
        
        # Данные
        self.original_array = []
        self.sorted_array = None
        self.current_state = None
        self.steps_generator = None
        self.is_playing = False
        self.speed = 1000  # миллисекунды между шагами
        
        # Создаем интерфейс (теперь окно входа НЕ показываем при запуске)
        self.create_widgets()
        
        # Обновляем статус авторизации
        self.update_auth_status()
    
    def show_login_dialog(self):
        """Показывает диалог авторизации."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Авторизация")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#f0f0f0')
        dialog.resizable(False, False)
        
        # Центрируем окно
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Заголовок
        title_label = tk.Label(
            dialog,
            text="Вход в систему",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=20)
        
        # Поля ввода
        input_frame = tk.Frame(dialog, bg='#f0f0f0')
        input_frame.pack(pady=20, padx=30, fill='x')
        
        tk.Label(input_frame, text="Имя пользователя:", font=('Arial', 10), bg='#f0f0f0', fg='#333').pack(anchor='w', pady=5)
        username_entry = tk.Entry(input_frame, font=('Arial', 12), width=30)
        username_entry.pack(fill='x', pady=5)
        username_entry.focus()
        
        tk.Label(input_frame, text="Пароль:", font=('Arial', 10), bg='#f0f0f0', fg='#333').pack(anchor='w', pady=5)
        password_entry = tk.Entry(input_frame, font=('Arial', 12), width=30, show='*')
        password_entry.pack(fill='x', pady=5)
        
        def login():
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            success, msg = self.auth_manager.login(username, password)
            if success:
                dialog.destroy()
                self.update_auth_status()
                messagebox.showinfo("Успех", msg)
            else:
                messagebox.showerror("Ошибка", msg)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            if not username or not password:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            success, msg = self.auth_manager.register(username, password)
            if success:
                messagebox.showinfo("Успех", msg)
                # Автоматически входим после регистрации
                success, msg = self.auth_manager.login(username, password)
                if success:
                    dialog.destroy()
                    self.update_auth_status()
                    messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
            else:
                messagebox.showerror("Ошибка", msg)
        
        # Кнопки
        button_frame = tk.Frame(dialog, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Войти",
            command=login,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)
        
        tk.Button(
            button_frame,
            text="Регистрация",
            command=register,
            bg='#2196F3',
            fg='white',
            font=('Arial', 11),
            padx=20,
            pady=8
        ).pack(side='left', padx=5)
        
        password_entry.bind('<Return>', lambda e: login())
        username_entry.bind('<Return>', lambda e: password_entry.focus())
    
    def create_widgets(self):
        """Создает элементы интерфейса."""
        # Верхняя панель с авторизацией
        top_frame = tk.Frame(self.root, bg='#e0e0e0', relief='raised', bd=2)
        top_frame.pack(fill='x', padx=0, pady=0)
        
        # Заголовок
        title_label = tk.Label(
            top_frame,
            text="ВИЗУАЛИЗАЦИЯ АЛГОРИТМА BUCKET SORT",
            font=('Arial', 16, 'bold'),
            bg='#e0e0e0',
            fg='#333'
        )
        title_label.pack(side='left', padx=20, pady=10)
        
        # Панель авторизации
        auth_frame = tk.Frame(top_frame, bg='#e0e0e0')
        auth_frame.pack(side='right', padx=20, pady=10)
        
        self.auth_status_label = tk.Label(
            auth_frame,
            text="Не авторизован",
            font=('Arial', 10),
            bg='#e0e0e0',
            fg='#666'
        )
        self.auth_status_label.pack(side='left', padx=10)
        
        self.login_button = tk.Button(
            auth_frame,
            text="Войти",
            command=self.show_login_dialog,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 9),
            padx=10,
            pady=3
        )
        self.login_button.pack(side='left', padx=2)
        
        self.logout_button = tk.Button(
            auth_frame,
            text="Выйти",
            command=self.logout,
            bg='#F44336',
            fg='white',
            font=('Arial', 9),
            padx=10,
            pady=3,
            state='disabled'
        )
        self.logout_button.pack(side='left', padx=2)
        
        # Панель управления
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10, fill='x', padx=20)
        
        # Кнопки ввода данных
        input_frame = tk.LabelFrame(control_frame, text="Ввод данных", bg='#f0f0f0', font=('Arial', 10), fg='#333')
        input_frame.pack(side='left', padx=10, fill='x', expand=True)
        
        tk.Button(
            input_frame,
            text="Ввести массив",
            command=self.input_array,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            input_frame,
            text="Сгенерировать случайный",
            command=self.generate_random,
            bg='#2196F3',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        tk.Button(
            input_frame,
            text="Загрузить из файла",
            command=self.load_from_file,
            bg='#FF9800',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5
        ).pack(side='left', padx=5)
        
        # Кнопки управления визуализацией
        play_frame = tk.LabelFrame(control_frame, text="Управление", bg='#f0f0f0', font=('Arial', 10), fg='#333')
        play_frame.pack(side='left', padx=10, fill='x', expand=True)
        
        self.start_button = tk.Button(
            play_frame,
            text="▶ Начать",
            command=self.start_visualization,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10,
            pady=5,
            state='disabled',
            disabledforeground='#E0E0E0'
        )
        self.start_button.pack(side='left', padx=5)
        
        self.pause_button = tk.Button(
            play_frame,
            text="⏸ Пауза",
            command=self.pause_visualization,
            bg='#fd9a21',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5,
            state='disabled',
            disabledforeground='#E0E0E0'
        )
        self.pause_button.pack(side='left', padx=5)
        
        self.reset_button = tk.Button(
            play_frame,
            text="↻ Сброс",
            command=self.reset_visualization,
            bg='#F44336',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5,
            state='disabled',
            disabledforeground='#E0E0E0'
        )
        self.reset_button.pack(side='left', padx=5)
        
        # Кнопки сохранения и истории
        save_frame = tk.LabelFrame(control_frame, text="История", bg='#f0f0f0', font=('Arial', 10), fg='#333')
        save_frame.pack(side='left', padx=10)
        
        self.save_button = tk.Button(
            save_frame,
            text="💾 Сохранить",
            command=self.save_sort_result,
            bg='#9C27B0',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5,
            state='disabled',
            disabledforeground='#E0E0E0'
        )
        self.save_button.pack(side='left', padx=5)
        
        self.history_button = tk.Button(
            save_frame,
            text="📋 История",
            command=self.show_history,
            bg='#fd7c6e',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5,
            state='disabled',
            disabledforeground='#E0E0E0'
        )
        self.history_button.pack(side='left', padx=5)
        
        # Скорость
        speed_frame = tk.LabelFrame(control_frame, text="Скорость", bg='#f0f0f0', font=('Arial', 10), fg='#333')
        speed_frame.pack(side='left', padx=10)
        
        self.speed_var = tk.IntVar(value=1000)
        speed_scale = tk.Scale(
            speed_frame,
            from_=50,
            to=2000,
            orient='horizontal',
            variable=self.speed_var,
            command=self.update_speed,
            length=150,
            bg='#f0f0f0',
            fg='#333',
            troughcolor='#e0e0e0',
            label="Медленно ← → Быстро"
        )
        speed_scale.pack()
        
        # Информационная панель
        info_frame = tk.Frame(self.root, bg='#e0e0e0', relief='raised', bd=2)
        info_frame.pack(pady=10, fill='x', padx=20)
        
        self.info_label = tk.Label(
            info_frame,
            text="Введите или загрузите массив для начала",
            font=('Arial', 11),
            bg='#e0e0e0',
            fg='#333',
            anchor='w',
            padx=10,
            pady=5
        )
        self.info_label.pack(fill='x')
        
        # Панель для отображения массива текстом (новый элемент для лучшей видимости)
        array_text_frame = tk.Frame(self.root, bg='white', relief='sunken', bd=1)
        array_text_frame.pack(pady=5, padx=20, fill='x')
        
        self.array_text_label = tk.Label(
            array_text_frame,
            text="Массив: не задан",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#333',
            anchor='w',
            padx=10,
            pady=5,
            wraplength=1150  # Перенос строки при длинном массиве
        )
        self.array_text_label.pack(fill='x')
        
        # Область визуализации
        canvas_frame = tk.Frame(self.root, bg='white', relief='sunken', bd=2)
        canvas_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Canvas для основного массива
        array_label = tk.Label(
            canvas_frame,
            text="Массив (графическое представление)",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#333'
        )
        array_label.pack(pady=5)
        
        self.array_canvas = tk.Canvas(
            canvas_frame,
            bg='white',
            height=200
        )
        self.array_canvas.pack(fill='x', padx=10, pady=5)
        
        # Canvas для ведер
        buckets_label = tk.Label(
            canvas_frame,
            text="Ведра",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#333'
        )
        buckets_label.pack(pady=5)
        
        # Scrollable frame для ведер
        buckets_container = tk.Frame(canvas_frame, bg='white')
        buckets_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.buckets_canvas = tk.Canvas(
            buckets_container,
            bg='white'
        )
        scrollbar = ttk.Scrollbar(buckets_container, orient="vertical", command=self.buckets_canvas.yview)
        self.buckets_scrollable_frame = tk.Frame(self.buckets_canvas, bg='white')
        
        self.buckets_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.buckets_canvas.configure(scrollregion=self.buckets_canvas.bbox("all"))
        )
        
        self.buckets_canvas.create_window((0, 0), window=self.buckets_scrollable_frame, anchor="nw")
        self.buckets_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.buckets_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка помощи (справка)
        help_button = tk.Button(
            self.root,
            text="❓ Помощь",
            command=self.show_help,
            bg='#009688',
            fg='white',
            font=('Arial', 9),
            padx=10,
            pady=3
        )
        help_button.pack(side='bottom', pady=5)
    
    def update_auth_status(self):
        """Обновляет статус авторизации в интерфейсе."""
        if self.auth_manager.is_authenticated():
            username = self.auth_manager.get_current_username()
            self.auth_status_label.config(text=f"Пользователь: {username}", fg='#2E7D32')
            self.login_button.config(state='disabled')
            self.logout_button.config(state='normal')
            self.history_button.config(state='normal')
        else:
            self.auth_status_label.config(text="Не авторизован", fg='#666')
            self.login_button.config(state='normal')
            self.logout_button.config(state='disabled')
            self.history_button.config(state='disabled')
    
    def logout(self):
        """Выполняет выход пользователя."""
        self.auth_manager.logout()
        self.update_auth_status()
        messagebox.showinfo("Выход", "Вы вышли из системы")
    
    def save_sort_result(self):
        """Сохраняет результат сортировки в базу данных."""
        if not self.auth_manager.is_authenticated():
            messagebox.showwarning("Предупреждение", "Необходимо авторизоваться для сохранения истории!")
            self.show_login_dialog()
            return
        
        if not self.original_array or self.sorted_array is None:
            messagebox.showwarning("Предупреждение", "Сначала выполните сортировку!")
            return
        
        user_id = self.auth_manager.get_current_user_id()
        success, msg = self.auth_manager.db.save_sort_history(
            user_id,
            self.original_array,
            self.sorted_array
        )
        
        if success:
            messagebox.showinfo("Успех", "Результат сохранен в историю!")
        else:
            messagebox.showerror("Ошибка", msg)
    
    def show_history(self):
        """Показывает историю сортировок пользователя."""
        if not self.auth_manager.is_authenticated():
            messagebox.showwarning("Предупреждение", "Необходимо авторизоваться для просмотра истории!")
            self.show_login_dialog()
            return
        
        user_id = self.auth_manager.get_current_user_id()
        history = self.auth_manager.db.get_sort_history(user_id)
        
        if not history:
            messagebox.showinfo("История", "История сортировок пуста")
            return
        
        # Создаем окно истории
        history_window = tk.Toplevel(self.root)
        history_window.title("История сортировок")
        history_window.geometry("800x600")
        history_window.configure(bg='#f0f0f0')
        
        # Центрируем окно
        history_window.update_idletasks()
        x = (history_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (history_window.winfo_screenheight() // 2) - (600 // 2)
        history_window.geometry(f"800x600+{x}+{y}")
        
        # Заголовок (теперь с темным текстом)
        tk.Label(
            history_window,
            text=f"История сортировок ({len(history)} записей)",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0',
            fg='#333'  # Темный текст вместо белого
        ).pack(pady=10)
        
        # Прокручиваемая область
        canvas = tk.Canvas(history_window, bg='white')
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Отображаем историю (улучшенный дизайн)
        for idx, record in enumerate(history):
            record_frame = tk.Frame(
                scrollable_frame,
                bg='#f5f5f5',
                relief='raised',
                bd=2
            )
            record_frame.pack(fill='x', padx=10, pady=5)
            
            # Заголовок записи
            tk.Label(
                record_frame,
                text=f"Запись #{len(history) - idx} | {record['created_at']}",
                font=('Arial', 10, 'bold'),
                bg='#f5f5f5',
                fg='#333'  # Темный текст
            ).pack(anchor='w', padx=10, pady=5)
            
            # Исходный массив
            orig_text = f"Исходный: {record['original_array']}"
            if len(orig_text) > 80:  # Если массив слишком длинный
                orig_text = f"Исходный: {record['original_array'][:10]}... ({len(record['original_array'])} элементов)"
            
            tk.Label(
                record_frame,
                text=orig_text,
                font=('Arial', 9),
                bg='#f5f5f5',
                fg='#333',  # Темный текст
                anchor='w',
                wraplength=750  # Перенос строки
            ).pack(fill='x', padx=10, pady=2)
            
            # Отсортированный массив
            sorted_text = f"Отсортированный: {record['sorted_array']}"
            if len(sorted_text) > 80:  # Если массив слишком длинный
                sorted_text = f"Отсортированный: {record['sorted_array'][:10]}... ({len(record['sorted_array'])} элементов)"
            
            tk.Label(
                record_frame,
                text=sorted_text,
                font=('Arial', 9),
                bg='#f5f5f5',
                fg='#333',  # Темный текст
                anchor='w',
                wraplength=750  # Перенос строки
            ).pack(fill='x', padx=10, pady=2)
            
            # Кнопка загрузки
            def load_array(orig_arr, sorted_arr):
                self.original_array = orig_arr
                self.sorted_array = sorted_arr
                self.reset_visualization()
                self.start_button.config(state='normal')
                self.array_text_label.config(text=f"Массив: {orig_arr}")
                history_window.destroy()
                messagebox.showinfo("Успех", "Массив загружен!")
            
            tk.Button(
                record_frame,
                text="Загрузить",
                command=lambda o=record['original_array'], s=record['sorted_array']: load_array(o, s),
                bg='#4CAF50',
                fg='white',
                font=('Arial', 9),
                padx=10,
                pady=3
            ).pack(anchor='e', padx=10, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Плавное появление окна
        history_window.withdraw()
        history_window.deiconify()
        history_window.update()
    
    def show_help(self):
        """Показывает справку по использованию приложения."""
        help_text = """
ВИЗУАЛИЗАЦИЯ BUCKET SORT - СПРАВКА

1. АВТОРИЗАЦИЯ:
   - Нажмите "Войти" для входа в систему
   - Используйте "Регистрация" для создания нового аккаунта
   - Авторизация необходима для сохранения истории сортировок

2. ВВОД ДАННЫХ:
   - "Ввести массив" - ввод чисел с клавиатуры через пробел
   - "Сгенерировать случайный" - автоматическая генерация массива
   - "Загрузить из файла" - загрузка из текстового файла

3. ВИЗУАЛИЗАЦИЯ:
   - "▶ Начать" - запуск визуализации сортировки
   - "⏸ Пауза" - приостановка визуализации
   - "↻ Сброс" - сброс к начальному состоянию
   - Регулятор скорости - изменение скорости анимации

4. СОХРАНЕНИЕ И ИСТОРИЯ:
   - "💾 Сохранить" - сохранение результата в историю (требуется авторизация)
   - "📋 История" - просмотр сохраненных сортировок

5. ПОМОЩЬ:
   - Нажмите "❓ Помощь" для отображения этой справки

Алгоритм Bucket Sort:
- Распределяет элементы по "ведрам" на основе их значений
- Сортирует каждое ведро отдельно
- Объединяет отсортированные ведра в итоговый массив
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Справка")
        help_window.geometry("600x500")
        help_window.configure(bg='#f0f0f0')
        
        # Центрируем окно
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (500 // 2)
        help_window.geometry(f"600x500+{x}+{y}")
        
        text_widget = tk.Text(
            help_window,
            wrap='word',
            font=('Arial', 10),
            bg='white',
            fg='#333',
            padx=15,
            pady=15
        )
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        tk.Button(
            help_window,
            text="Закрыть",
            command=help_window.destroy,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 11),
            padx=20,
            pady=5
        ).pack(pady=10)
    
    def input_array(self):
        """Ввод массива с клавиатуры."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Ввод массива")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#f0f0f0')
        
        tk.Label(
            dialog,
            text=f"Введите элементы массива через пробел (максимум {self.MAX_ARRAY_SIZE} элементов):",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#333'
        ).pack(pady=10)
        
        entry = tk.Entry(dialog, font=('Arial', 12), width=40)
        entry.pack(pady=5)
        entry.focus()
        
        def ok():
            try:
                arr = [int(x) for x in entry.get().strip().split()]
                if not arr:
                    messagebox.showerror("Ошибка", "Массив не может быть пустым!")
                elif len(arr) > self.MAX_ARRAY_SIZE:
                    messagebox.showerror(
                        "Ошибка",
                        f"Размер массива превышает максимально допустимый!\n"
                        f"Максимум: {self.MAX_ARRAY_SIZE} элементов\n"
                        f"Введено: {len(arr)} элементов"
                    )
                else:
                    self.original_array = arr
                    self.sorted_array = None
                    self.reset_visualization()
                    self.start_button.config(state='normal')
                    self.array_text_label.config(text=f"Массив: {arr}")
                    dialog.destroy()
                    self.info_label.config(text=f"Массив загружен: {arr}")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите только целые числа!")
        
        tk.Button(
            dialog, 
            text="OK", 
            command=ok, 
            bg='#4CAF50', 
            fg='white', 
            padx=20
        ).pack(pady=10)
        entry.bind('<Return>', lambda e: ok())
    
    def generate_random(self):
        """Генерация случайного массива."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Генерация массива")
        dialog.geometry("450x300")  # Увеличили высоту для валидации
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg='#f0f0f0')
        
        # Контейнер для полей ввода
        content_frame = tk.Frame(dialog, bg='#f0f0f0')
        content_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Размер массива
        size_frame = tk.Frame(content_frame, bg='#f0f0f0')
        size_frame.pack(fill='x', pady=5)
        tk.Label(
            size_frame,
            text=f"Размер массива (1-{self.MAX_ARRAY_SIZE}):",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left', padx=5)
        size_entry = tk.Entry(size_frame, font=('Arial', 12), width=15)
        size_entry.pack(side='left', padx=5)
        size_entry.insert(0, "20")
        
        # Минимальное значение
        min_frame = tk.Frame(content_frame, bg='#f0f0f0')
        min_frame.pack(fill='x', pady=5)
        tk.Label(
            min_frame, 
            text="Минимальное значение:", 
            font=('Arial', 10), 
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left', padx=5)
        min_entry = tk.Entry(min_frame, font=('Arial', 12), width=15)
        min_entry.pack(side='left', padx=5)
        min_entry.insert(0, "1")
        
        # Максимальное значение
        max_frame = tk.Frame(content_frame, bg='#f0f0f0')
        max_frame.pack(fill='x', pady=5)
        tk.Label(
            max_frame, 
            text="Максимальное значение:", 
            font=('Arial', 10), 
            bg='#f0f0f0',
            fg='#333'
        ).pack(side='left', padx=5)
        max_entry = tk.Entry(max_frame, font=('Arial', 12), width=15)
        max_entry.pack(side='left', padx=5)
        max_entry.insert(0, "100")
        
        # Label для отображения ошибок валидации
        validation_label = tk.Label(
            content_frame,
            text="",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#F44336',
            wraplength=400
        )
        validation_label.pack(pady=10)
        
        def validate_inputs():
            """Проверяет корректность введенных значений."""
            try:
                size = int(size_entry.get())
                min_val = int(min_entry.get())
                max_val = int(max_entry.get())
                
                errors = []
                
                if size <= 0:
                    errors.append("Размер массива должен быть положительным числом!")
                elif size > self.MAX_ARRAY_SIZE:
                    errors.append(f"Размер массива не должен превышать {self.MAX_ARRAY_SIZE}!")
                
                if min_val > max_val:
                    errors.append("Минимальное значение не может быть больше максимального!")
                
                # Дополнительная проверка: минимальное не должно быть слишком большим
                if min_val > 1000000 or max_val > 1000000:
                    errors.append("Значения не должны превышать 1,000,000!")
                
                if min_val < -1000000 or max_val < -1000000:
                    errors.append("Значения не должны быть меньше -1,000,000!")
                
                if errors:
                    validation_label.config(text="\n".join(errors))
                    return False
                else:
                    validation_label.config(text="")
                    return True
                
            except ValueError:
                validation_label.config(text="Все поля должны содержать целые числа!")
                return False
        
        def generate():
            if validate_inputs():
                try:
                    size = int(size_entry.get())
                    min_val = int(min_entry.get())
                    max_val = int(max_entry.get())
                    
                    self.original_array = [random.randint(min_val, max_val) for _ in range(size)]
                    self.sorted_array = None
                    self.reset_visualization()
                    self.start_button.config(state='normal')
                    self.array_text_label.config(text=f"Массив: {self.original_array}")
                    dialog.destroy()
                    self.info_label.config(text=f"Сгенерирован массив из {size} элементов")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при генерации: {e}")
        
        # Кнопки
        button_frame = tk.Frame(dialog, bg='#f0f0f0')
        button_frame.pack(pady=15)
        
        generate_button = tk.Button(
            button_frame,
            text="Сгенерировать",
            command=generate,
            bg='#2196F3',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=25,
            pady=8
        )
        generate_button.pack(side='left', padx=5)
        
        cancel_button = tk.Button(
            button_frame,
            text="Отмена",
            command=dialog.destroy,
            bg='#757575',
            fg='white',
            font=('Arial', 11),
            padx=25,
            pady=8
        )
        cancel_button.pack(side='left', padx=5)
        
        # Валидация при вводе
        def on_entry_change(*args):
            validate_inputs()
        
        size_entry.bind('<KeyRelease>', on_entry_change)
        min_entry.bind('<KeyRelease>', on_entry_change)
        max_entry.bind('<KeyRelease>', on_entry_change)
        
        # Фокус на первом поле и обработка Enter
        size_entry.focus()
        size_entry.bind('<Return>', lambda e: min_entry.focus())
        min_entry.bind('<Return>', lambda e: max_entry.focus())
        max_entry.bind('<Return>', lambda e: generate())
    
    def load_from_file(self):
        """Загрузка массива из файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    numbers = []
                    for line in content.split('\n'):
                        numbers.extend([int(x) for x in line.split() if x.strip()])
                    if not numbers:
                        messagebox.showerror("Ошибка", "Файл не содержит чисел!")
                    elif len(numbers) > self.MAX_ARRAY_SIZE:
                        messagebox.showerror(
                            "Ошибка",
                            f"Размер массива в файле превышает максимально допустимый!\n"
                            f"Максимум: {self.MAX_ARRAY_SIZE} элементов\n"
                            f"В файле: {len(numbers)} элементов"
                        )
                    else:
                        self.original_array = numbers
                        self.sorted_array = None
                        self.reset_visualization()
                        self.start_button.config(state='normal')
                        self.array_text_label.config(text=f"Массив: {numbers}")
                        self.info_label.config(text=f"Загружено {len(numbers)} элементов из файла")
            except ValueError:
                messagebox.showerror("Ошибка", "Файл должен содержать только целые числа!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке файла: {e}")
    
    def start_visualization(self):
        """Запускает визуализацию."""
        if not self.original_array:
            messagebox.showerror("Ошибка", "Сначала загрузите массив!")
            return
        
        if self.steps_generator is None:
            self.steps_generator = bucket_sort_with_steps(self.original_array.copy())
            # Выполняем сортировку для сохранения результата
            self.sorted_array = bucket_sort(self.original_array.copy())
        
        self.is_playing = True
        self.start_button.config(state='disabled')
        self.pause_button.config(state='normal')
        self.reset_button.config(state='normal')
        
        self.visualization_thread()
    
    def visualization_thread(self):
        """Поток для визуализации."""
        def run():
            try:
                while self.is_playing:
                    try:
                        state = next(self.steps_generator)
                        self.root.after(0, lambda s=state: self.update_visualization(s))
                        time.sleep(self.speed / 1000.0)
                    except StopIteration:
                        self.root.after(0, self.visualization_complete)
                        break
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Ошибка", str(e)))
        
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
    
    def pause_visualization(self):
        """Приостанавливает визуализацию."""
        self.is_playing = False
        self.start_button.config(state='normal', text="▶ Продолжить")
        self.pause_button.config(state='disabled')
    
    def reset_visualization(self):
        """Сбрасывает визуализацию."""
        self.is_playing = False
        self.steps_generator = None
        self.current_state = None
        self.start_button.config(state='normal', text="▶ Начать")
        self.pause_button.config(state='disabled')
        self.reset_button.config(state='disabled')
        self.save_button.config(state='disabled' if self.sorted_array is None else 'normal')
        self.clear_canvas()
        if self.original_array:
            self.info_label.config(text=f"Готов к визуализации. Массив: {self.original_array}")
    
    def update_speed(self, value):
        """Обновляет скорость визуализации."""
        slider_value = int(value)
        self.speed = 2050 - slider_value
    
    def visualization_complete(self):
        """Вызывается при завершении визуализации."""
        self.is_playing = False
        self.start_button.config(state='normal', text="▶ Начать")
        self.pause_button.config(state='disabled')
        self.save_button.config(state='normal')
        self.info_label.config(text=f"Сортировка завершена! Отсортированный массив: {self.sorted_array}")
        messagebox.showinfo("Завершено", "Визуализация завершена!")
    
    def clear_canvas(self):
        """Очищает canvas."""
        self.array_canvas.delete("all")
        for widget in self.buckets_scrollable_frame.winfo_children():
            widget.destroy()
    
    def update_visualization(self, state):
        """Обновляет визуализацию на основе текущего состояния."""
        self.current_state = state
        
        # Обновляем информацию
        self.info_label.config(text=f"Шаг {state['step']}: {state['description']}")
        
        # Обновляем текстовое отображение массива
        if state['array']:
            array_text = f"Текущий массив: {state['array']}"
            if len(array_text) > 120:  # Если массив слишком длинный
                array_text = f"Массив: {state['array'][:10]}... ({len(state['array'])} элементов)"
            self.array_text_label.config(text=array_text)
        
        # Очищаем canvas
        self.array_canvas.delete("all")
        
        # Рисуем основной массив
        array = state['array']
        if array:
            canvas_width = self.array_canvas.winfo_width() or 800
            canvas_height = 180
            bar_width = max(10, (canvas_width - 20) / len(array) - 2)  # Увеличили минимальную ширину
            max_val = max(array) if array else 1
            min_val = min(array) if array else 0
            range_val = max_val - min_val if max_val != min_val else 1
            
            for i, value in enumerate(array):
                x = 10 + i * (bar_width + 2)
                height = int((value - min_val) / range_val * (canvas_height - 60)) + 30  # Увеличили высоту
                y = canvas_height - height
                
                # Цвет зависит от того, сравнивается ли элемент
                color = '#4CAF50'  # зеленый по умолчанию
                if state['comparing']:
                    if isinstance(state['comparing'], tuple):
                        if i in state['comparing']:
                            color = '#F44336'  # красный для сравниваемых
                    elif i == state['comparing']:
                        color = '#FFC107'  # желтый для текущего
                
                # Рисуем столбец с тенью для лучшей видимости
                self.array_canvas.create_rectangle(
                    x, y, x + bar_width, canvas_height - 10,
                    fill=color,
                    outline='#333',
                    width=2
                )
                
                # Подпись значения (увеличили шрифт для лучшей читаемости)
                self.array_canvas.create_text(
                    x + bar_width / 2, canvas_height - 20,
                    text=str(value),
                    font=('Arial', 10, 'bold'),
                    fill='#333'
                )
                
                # Подпись индекса
                self.array_canvas.create_text(
                    x + bar_width / 2, canvas_height - 5,
                    text=f"[{i}]",
                    font=('Arial', 8),
                    fill='#666'
                )
        
        # Рисуем ведра
        for widget in self.buckets_scrollable_frame.winfo_children():
            widget.destroy()
        
        buckets = state['buckets']
        if buckets:
            current_bucket = state['current_bucket']
            
            for idx, bucket in enumerate(buckets):
                bucket_frame = tk.Frame(
                    self.buckets_scrollable_frame,
                    bg='#e8f5e9' if idx == current_bucket else '#f5f5f5',
                    relief='raised',
                    bd=2
                )
                bucket_frame.pack(fill='x', padx=5, pady=5)
                
                tk.Label(
                    bucket_frame,
                    text=f"Ведро {idx} ({len(bucket)} элементов): {bucket}",
                    font=('Arial', 10, 'bold'),
                    bg=bucket_frame['bg'],
                    fg='#333',
                    anchor='w',
                    wraplength=750  # Перенос строки для длинных массивов
                ).pack(anchor='w', padx=5, pady=2)
                
                if bucket:
                    bucket_canvas = tk.Canvas(bucket_frame, height=100, bg=bucket_frame['bg'])  # Увеличили высоту
                    bucket_canvas.pack(fill='x', padx=5, pady=5)
                    
                    canvas_width = 700
                    bar_width = max(5, (canvas_width - 20) / len(bucket) - 1)
                    max_val = max(bucket) if bucket else 1
                    min_val = min(bucket) if bucket else 0
                    range_val = max_val - min_val if max_val != min_val else 1
                    
                    for i, value in enumerate(bucket):
                        x = 10 + i * (bar_width + 1)
                        height = int((value - min_val) / range_val * 70) + 20  # Увеличили масштаб
                        y = 90 - height
                        
                        color = '#2196F3'
                        if state['comparing'] and isinstance(state['comparing'], tuple):
                            if idx == current_bucket and i in state['comparing']:
                                color = '#F44336'
                        
                        bucket_canvas.create_rectangle(
                            x, y, x + bar_width, 90,
                            fill=color,
                            outline='#333',
                            width=1
                        )
                        bucket_canvas.create_text(
                            x + bar_width / 2, 95,
                            text=str(value),
                            font=('Arial', 8),
                            fill='#333'
                        )
                else:
                    tk.Label(
                        bucket_frame,
                        text="Пусто",
                        font=('Arial', 10),
                        fg='#999',
                        bg=bucket_frame['bg']
                    ).pack(pady=10)
        
        self.root.update_idletasks()


def main():
    """Главная функция для запуска приложения."""
    root = tk.Tk()
    app = BucketSortVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()