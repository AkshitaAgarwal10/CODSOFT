import tkinter as tk
from tkinter import ttk, messagebox
import json, os

DATA_FILE = "tasks.json"

class StyledToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎨 Styled To‑Do List")
        self.geometry("420x540")
        self.configure(bg="#ddebef")  
        self.tasks = []
        self.load_tasks()
        self.setup_style()
        self.build_ui()
        self.refresh_tasks()
        self.update_status()

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam") 
        style.configure("Accent.TButton",
                        font=("Segoe UI", 11, "bold"),
                        foreground="white", background="#5DADE2")
        style.map("Accent.TButton",
                  background=[("active", "#3498DB")])
        style.configure("Task.TCheckbutton",
                        font=("Segoe UI", 12),
                        foreground="#333333",
                        background="#FDFEFE")
        style.map("Task.TCheckbutton",
                  foreground=[("selected", "#888888")],
                  background=[("active", "#ececec")])

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try: self.tasks = json.load(f)
                except json.JSONDecodeError: self.tasks = []

    def save_tasks(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def build_ui(self):
        top = ttk.Frame(self)
        top.pack(pady=20)
        self.entry = ttk.Entry(top, font=("Segoe UI", 13), width=30)
        self.entry.pack(side="left", padx=(0,10))
        self.entry.bind("<Return>", lambda e: self.add_task())
        ttk.Button(top, text="Add Task", style="Accent.TButton", width=10,
                   command=self.add_task).pack(side="left")

        container = ttk.Frame(self, padding=5, relief="solid")
        container.pack(padx=20, pady=10, fill="both", expand=True)
        self.canvas = tk.Canvas(container, bg="#FDFEFE", highlightthickness=0)
        self.scroll = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        bottom = ttk.Frame(self)
        bottom.pack(pady=15)
        ttk.Button(bottom, text="Clear Done", style="Accent.TButton", command=self.clear_completed).pack(side="left", padx=5)
        ttk.Button(bottom, text="Clear All", style="Accent.TButton", command=self.clear_all).pack(side="left", padx=5)

        self.status = ttk.Label(self, font=("Segoe UI", 11))
        self.status.pack(pady=5)

    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Enter a task.")
            return
        self.tasks.append({"text": text, "done": False})
        self.entry.delete(0, "end")
        self.save_tasks()
        self.refresh_tasks()
        self.update_status()

    def toggle_task(self, idx, var):
        self.tasks[idx]["done"] = bool(var.get())
        self.save_tasks()
        self.refresh_tasks()
        self.update_status()

    def delete_task(self, idx):
        self.tasks.pop(idx)
        self.save_tasks()
        self.refresh_tasks()
        self.update_status()

    def clear_completed(self):
        self.tasks = [t for t in self.tasks if not t["done"]]
        self.save_tasks()
        self.refresh_tasks()
        self.update_status()

    def clear_all(self):
        if messagebox.askyesno("Confirm", "Delete all tasks?"):
            self.tasks.clear()
            self.save_tasks()
            self.refresh_tasks()
            self.update_status()

    def refresh_tasks(self):
        for w in self.inner.winfo_children():
            w.destroy()
        for i, t in enumerate(self.tasks):
            var = tk.IntVar(value=t["done"])
            chk = ttk.Checkbutton(self.inner, text=t["text"], variable=var,
                                  style="Task.TCheckbutton",
                                  command=lambda i=i, v=var: self.toggle_task(i, v))
            chk.grid(row=i, column=0, sticky="w", pady=3)
            del_btn = ttk.Button(self.inner, text="✖", width=3,
                                 style="Accent.TButton",
                                 command=lambda i=i: self.delete_task(i))
            del_btn.grid(row=i, column=1, padx=5)

    def update_status(self):
        total = len(self.tasks)
        done = sum(t["done"] for t in self.tasks)
        self.status.config(text=f"✅ {done} done · 🕓 {total-done} remaining · 📋 {total} total")

if __name__ == "__main__":
    StyledToDoApp().mainloop()
