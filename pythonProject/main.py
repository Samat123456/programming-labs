import tkinter as tk
from tkinter import ttk, messagebox

class Task:
    def __init__(self, name: str, priority: int, duration: int):
        self.name = name
        self.priority = priority
        self.duration = duration

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int):
        if not (1 <= value <= 5):
            raise ValueError("Приоритет задачи должен быть в диапазоне от 1 до 5!")
        self._value = value
        self._priority = value

    def __str__(self):
        return f"Задача '{self.name}' (Приоритет: {self.priority}, Длительность: {self.duration})"

class Robot:
    def __init__(self, name: str):
        self.name = name
        self.current_task = None

    @property
    def status(self) -> str:
        if self.current_task:
            return f"Занят ({self.current_task.name})"
        return "Свободен"

    def can_take_task(self, task: Task) -> bool:
        return self.current_task is None

    def assign_task(self, task: Task):
        if not self.can_take_task(task):
            raise ValueError(f"Робот {self.name} не может взять эту задачу!")
        self.current_task = task

    def __str__(self):
        return f"Робот {self.name} -> Статус: {self.status}"

class TransportRobot(Robot):
    def __init__(self, name: str, max_payload: float = 50.0):
        super().__init__(name)
        self.max_payload = max_payload

    def can_take_task(self, task: Task) -> bool:
        if self.current_task is not None:
            return False
        transport_keywords = ["доставка", "перевозка", "склад", "груз", "транспортировка"]
        task_name_lower = task.name.lower()
        return any(keyword in task_name_lower for keyword in transport_keywords)

    def __str__(self):
        base_str = super().__str__()
        return f"[Транспорт] {base_str} (Грузоподъемность: {self.max_payload} кг)"

class DispatcherApp(tk.Tk):
    def __init__(self, robots_list: list):
        super().__init__()
        self.title("Диспетчер задач роботов")
        self.geometry("750x500")
        self.resizable(False, False)
        self.robots = robots_list
        self.tasks_pool = []
        self._build_widgets()
        self._update_robots_view()

    def _build_widgets(self):
        form_frame = ttk.LabelFrame(self, text=" Добавление новой задачи ")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(form_frame, text="Название задачи:").pack(anchor="w", padx=5, pady=2)
        self.entry_name = ttk.Entry(form_frame, width=25)
        self.entry_name.pack(fill="x", padx=5, pady=2)
        self.entry_name.insert(0, "Доставка деталей")

        ttk.Label(form_frame, text="Приоритет (1-5):").pack(anchor="w", padx=5, pady=2)
        self.combo_priority = ttk.Combobox(form_frame, values=["1", "2", "3", "4", "5"], state="readonly")
        self.combo_priority.current(2)
        self.combo_priority.pack(fill="x", padx=5, pady=2)

        ttk.Label(form_frame, text="Длительность (ед.):").pack(anchor="w", padx=5, pady=2)
        self.entry_duration = ttk.Entry(form_frame, width=25)
        self.entry_duration.pack(fill="x", padx=5, pady=2)
        self.entry_duration.insert(0, "10")

        ttk.Button(form_frame, text="Создать задачу", command=self._on_add_task).pack(fill="x", padx=5, pady=10)
        ttk.Button(form_frame, text="Назначить свободным роботам", command=self._on_dispatch).pack(fill="x", padx=5, pady=2)

        table_frame = ttk.LabelFrame(self, text=" Текущая очередь задач ")
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(table_frame, columns=("name", "priority", "duration"), show="headings", height=8)
        self.tree.heading("name", text="Название")
        self.tree.heading("priority", text="Приоритет")
        self.tree.heading("duration", text="Длительность")
        self.tree.column("name", width=180)
        self.tree.column("priority", width=90, anchor="center")
        self.tree.column("duration", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        bottom_frame = ttk.LabelFrame(self, text=" Мониторинг роботов и Журнал событий ")
        bottom_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.robots_text = tk.Text(bottom_frame, width=38, height=10, font=("Consolas", 10), bg="#f8f9fa")
        self.robots_text.pack(side="left", padx=5, pady=5, fill="y")

        self.log_text = tk.Text(bottom_frame, width=54, height=10, font=("Consolas", 10), bg="#f0f4f8")
        self.log_text.pack(side="right", padx=5, pady=5, fill="both", expand=True)

        self._log("Система запущена. Диспетчер готов к работе.")

    def _log(self, message: str):
        self.log_text.insert(tk.END, f">> {message}\n")
        self.log_text.see(tk.END)

    def _update_robots_view(self):
        self.robots_text.delete("1.0", tk.END)
        self.robots_text.insert(tk.END, "СТАТУС ИСПОЛНИТЕЛЕЙ:\n")
        self.robots_text.insert(tk.END, "=" * 35 + "\n")
        for r in self.robots:
            self.robots_text.insert(tk.END, f"{r}\n\n")

    def _update_tasks_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks_pool:
            self.tree.insert("", tk.END, values=(task.name, task.priority, task.duration))

    def _on_add_task(self):
        try:
            name = self.entry_name.get().strip()
            if not name:
                raise ValueError("Название задачи не может быть пустым!")
            priority = int(self.combo_priority.get())
            duration = int(self.entry_duration.get().strip())
            if duration <= 0:
                raise ValueError("Длительность работы должна быть больше 0!")

            new_task = Task(name, priority, duration)
            self.tasks_pool.append(new_task)
            self.tasks_pool.sort(key=lambda t: t.priority, reverse=True)
            self._update_tasks_table()
            self._log(f"Добавлена задача: {new_task.name} (P:{priority})")
            self.entry_name.delete(0, tk.END)
        except ValueError as err:
            messagebox.showerror("Ошибка валидации", f"Некорректный ввод:\n{err}")

    def _on_dispatch(self):
        if not self.tasks_pool:
            messagebox.showinfo("Инфо", "Очередь задач пуста!")
            return
        assigned_any = False
        remaining_tasks = list(self.tasks_pool)
        for task in remaining_tasks:
            for robot in self.robots:
                if robot.can_take_task(task):
                    robot.assign_task(task)
                    self.tasks_pool.remove(task)
                    self._log(f"Успех: Роботу '{robot.name}' поручена задача '{task.name}'")
                    assigned_any = True
                    break
        if assigned_any:
            self._update_tasks_table()
            self._update_robots_view()
        else:
            self._log("Внимание: Ни один робот не смог взять задачи из очереди.")

def main():
    fleet = [
        Robot(name="Universal-01"),
        TransportRobot(name="Transporter-Heavy", max_payload=150.0),
        Robot(name="Universal-02"),
        TransportRobot(name="AGV-Sklad", max_payload=40.0)
    ]
    app = DispatcherApp(robots_list=fleet)
    app.mainloop()

if __name__ == "__main__":
    main()
