"""
GUI приложение для визуализации алгоритма Bucket Sort.

Использует Tkinter для создания графического интерфейса с анимацией процесса сортировки.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import threading
import time
from bucket_sort_visualizer import bucket_sort_with_steps


class BucketSortVisualizer:
    """Класс для визуализации алгоритма Bucket Sort."""
    
    MAX_ARRAY_SIZE = 100  # Максимальный размер массива для визуализации
    
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализация Bucket Sort")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Данные
        self.original_array = []
        self.current_state = None
        self.steps_generator = None
        self.is_playing = False
        self.speed = 1000  # миллисекунды между шагами (инвертировано: больше значение = быстрее)
        
        # Создаем интерфейс
        self.create_widgets()
        
    def create_widgets(self):
        """Создает элементы интерфейса."""
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="ВИЗУАЛИЗАЦИЯ АЛГОРИТМА BUCKET SORT",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=10)
        
        # Панель управления
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10, fill='x', padx=20)
        
        # Кнопки ввода данных
        input_frame = tk.LabelFrame(control_frame, text="Ввод данных", bg='#f0f0f0', font=('Arial', 10))
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
        play_frame = tk.LabelFrame(control_frame, text="Управление", bg='#f0f0f0', font=('Arial', 10))
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
            state='disabled'
        )
        self.start_button.pack(side='left', padx=5)
        
        self.pause_button = tk.Button(
            play_frame,
            text="⏸ Пауза",
            command=self.pause_visualization,
            bg='#FFC107',
            fg='white',
            font=('Arial', 10),
            padx=10,
            pady=5,
            state='disabled'
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
            state='disabled'
        )
        self.reset_button.pack(side='left', padx=5)
        
        # Скорость
        speed_frame = tk.LabelFrame(control_frame, text="Скорость", bg='#f0f0f0', font=('Arial', 10))
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
        
        # Область визуализации
        canvas_frame = tk.Frame(self.root, bg='white', relief='sunken', bd=2)
        canvas_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Canvas для основного массива
        array_label = tk.Label(
            canvas_frame,
            text="Массив",
            font=('Arial', 12, 'bold'),
            bg='white'
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
            bg='white'
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
        
    def input_array(self):
        """Ввод массива с клавиатуры."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Ввод массива")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text=f"Введите элементы массива через пробел (максимум {self.MAX_ARRAY_SIZE} элементов):",
            font=('Arial', 10)
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
                    self.reset_visualization()
                    self.start_button.config(state='normal')
                    dialog.destroy()
                    messagebox.showinfo("Успех", f"Массив загружен: {arr}")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите только целые числа!")
        
        tk.Button(dialog, text="OK", command=ok, bg='#4CAF50', fg='white', padx=20).pack(pady=10)
        entry.bind('<Return>', lambda e: ok())
    
    def generate_random(self):
        """Генерация случайного массива."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Генерация массива")
        dialog.geometry("450x250")
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
            text=f"Размер массива (макс. {self.MAX_ARRAY_SIZE}):",
            font=('Arial', 10),
            bg='#f0f0f0'
        ).pack(side='left', padx=5)
        size_entry = tk.Entry(size_frame, font=('Arial', 12), width=15)
        size_entry.pack(side='left', padx=5)
        size_entry.insert(0, "20")
        
        # Минимальное значение
        min_frame = tk.Frame(content_frame, bg='#f0f0f0')
        min_frame.pack(fill='x', pady=5)
        tk.Label(min_frame, text="Минимальное значение:", font=('Arial', 10), bg='#f0f0f0').pack(side='left', padx=5)
        min_entry = tk.Entry(min_frame, font=('Arial', 12), width=15)
        min_entry.pack(side='left', padx=5)
        min_entry.insert(0, "1")
        
        # Максимальное значение
        max_frame = tk.Frame(content_frame, bg='#f0f0f0')
        max_frame.pack(fill='x', pady=5)
        tk.Label(max_frame, text="Максимальное значение:", font=('Arial', 10), bg='#f0f0f0').pack(side='left', padx=5)
        max_entry = tk.Entry(max_frame, font=('Arial', 12), width=15)
        max_entry.pack(side='left', padx=5)
        max_entry.insert(0, "100")
        
        def generate():
            try:
                size = int(size_entry.get())
                min_val = int(min_entry.get())
                max_val = int(max_entry.get())
                if size <= 0:
                    messagebox.showerror("Ошибка", "Размер массива должен быть положительным числом!")
                elif size > self.MAX_ARRAY_SIZE:
                    messagebox.showerror(
                        "Ошибка",
                        f"Размер массива превышает максимально допустимый!\n"
                        f"Максимум: {self.MAX_ARRAY_SIZE} элементов\n"
                        f"Введено: {size} элементов"
                    )
                elif min_val > max_val:
                    messagebox.showerror("Ошибка", "Минимальное значение не может быть больше максимального!")
                else:
                    self.original_array = [random.randint(min_val, max_val) for _ in range(size)]
                    self.reset_visualization()
                    self.start_button.config(state='normal')
                    dialog.destroy()
                    messagebox.showinfo("Успех", f"Сгенерирован массив из {size} элементов")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите целые числа!")
        
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
                        self.reset_visualization()
                        self.start_button.config(state='normal')
                        messagebox.showinfo("Успех", f"Загружено {len(numbers)} элементов")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при загрузке файла: {e}")
    
    def start_visualization(self):
        """Запускает визуализацию."""
        if not self.original_array:
            messagebox.showerror("Ошибка", "Сначала загрузите массив!")
            return
        
        if self.steps_generator is None:
            self.steps_generator = bucket_sort_with_steps(self.original_array.copy())
        
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
        self.clear_canvas()
        if self.original_array:
            self.info_label.config(text=f"Готов к визуализации. Массив: {self.original_array}")
    
    def update_speed(self, value):
        """Обновляет скорость визуализации.
        
        Инвертированная логика: большее значение ползунка = быстрее (меньше задержка).
        Формула: delay = 2050 - value
        При value=50 -> delay=2000 (медленно)
        При value=2000 -> delay=50 (быстро)
        """
        slider_value = int(value)
        # Инвертируем: больше значение = меньше задержка = быстрее
        self.speed = 2050 - slider_value
    
    def visualization_complete(self):
        """Вызывается при завершении визуализации."""
        self.is_playing = False
        self.start_button.config(state='normal', text="▶ Начать")
        self.pause_button.config(state='disabled')
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
        
        # Очищаем canvas
        self.array_canvas.delete("all")
        
        # Рисуем основной массив
        array = state['array']
        if array:
            canvas_width = self.array_canvas.winfo_width() or 800
            canvas_height = 180
            bar_width = max(5, (canvas_width - 20) / len(array) - 2)
            max_val = max(array) if array else 1
            min_val = min(array) if array else 0
            range_val = max_val - min_val if max_val != min_val else 1
            
            for i, value in enumerate(array):
                x = 10 + i * (bar_width + 2)
                height = int((value - min_val) / range_val * (canvas_height - 40)) + 20
                y = canvas_height - height
                
                # Цвет зависит от того, сравнивается ли элемент
                color = '#4CAF50'  # зеленый по умолчанию
                if state['comparing']:
                    if isinstance(state['comparing'], tuple):
                        if i in state['comparing']:
                            color = '#F44336'  # красный для сравниваемых
                    elif i == state['comparing']:
                        color = '#FFC107'  # желтый для текущего
                
                self.array_canvas.create_rectangle(
                    x, y, x + bar_width, canvas_height - 10,
                    fill=color,
                    outline='#333',
                    width=1
                )
                # Подпись значения
                self.array_canvas.create_text(
                    x + bar_width / 2, canvas_height - 5,
                    text=str(value),
                    font=('Arial', 8),
                    fill='#333'
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
                    text=f"Ведро {idx} ({len(bucket)} элементов)",
                    font=('Arial', 10, 'bold'),
                    bg=bucket_frame['bg']
                ).pack(anchor='w', padx=5, pady=2)
                
                if bucket:
                    bucket_canvas = tk.Canvas(bucket_frame, height=80, bg=bucket_frame['bg'])
                    bucket_canvas.pack(fill='x', padx=5, pady=5)
                    
                    canvas_width = 700
                    bar_width = max(3, (canvas_width - 20) / len(bucket) - 1)
                    max_val = max(bucket)
                    min_val = min(bucket)
                    range_val = max_val - min_val if max_val != min_val else 1
                    
                    for i, value in enumerate(bucket):
                        x = 10 + i * (bar_width + 1)
                        height = int((value - min_val) / range_val * 50) + 10
                        y = 70 - height
                        
                        color = '#2196F3'
                        if state['comparing'] and isinstance(state['comparing'], tuple):
                            if idx == current_bucket and i in state['comparing']:
                                color = '#F44336'
                        
                        bucket_canvas.create_rectangle(
                            x, y, x + bar_width, 70,
                            fill=color,
                            outline='#333',
                            width=1
                        )
                        bucket_canvas.create_text(
                            x + bar_width / 2, 75,
                            text=str(value),
                            font=('Arial', 7),
                            fill='#333'
                        )
                else:
                    tk.Label(
                        bucket_frame,
                        text="Пусто",
                        font=('Arial', 9),
                        fg='#999',
                        bg=bucket_frame['bg']
                    ).pack(pady=5)
        
        self.root.update_idletasks()


def main():
    """Главная функция для запуска приложения."""
    root = tk.Tk()
    app = BucketSortVisualizer(root)
    root.mainloop()


if __name__ == "__main__":
    main()

