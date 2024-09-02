import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from PIL import Image, ImageTk

# File where tasks are stored
TODO_FILE = 'todos.json'

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        
        # Set window size and disable resizing
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        
        # Set the background color
        self.root.configure(bg='#e0e0e0')

        # Load and set the icon
        try:
            image = Image.open("todo.png")
            image_icon = ImageTk.PhotoImage(image)
            self.root.iconphoto(False, image_icon)
        except Exception as e:
            print(f"Error loading image: {e}")

        self.todos = self.load_todos()

        # Task list
        self.listbox_frame = tk.Frame(root, bg='#e0e0e0')
        self.listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.listbox_frame, width=470, bg='#e0e0e0', scrollregion=(0, 0, 470, 400))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.listbox_inner_frame = tk.Frame(self.canvas, bg='#e0e0e0')
        self.canvas.create_window((0, 0), window=self.listbox_inner_frame, anchor='nw')

        self.update_listbox()

        # Add task
        self.entry_frame = tk.Frame(root, bg='#e0e0e0')
        self.entry_frame.pack(pady=5)

        self.entry = tk.Entry(self.entry_frame, width=30, font=('Arial', 12), bg='#ffffff', fg='black')
        self.entry.insert(0, "Enter task")
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.set_placeholder)
        self.entry.bind("<Return>", self.add_todo_event)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.entry_frame, text="Add Task", command=self.add_todo, font=('Arial', 12), bg='#4CAF50', fg='white', width=10)
        self.add_button.pack(side=tk.LEFT, padx=5)

        # Delete selected tasks
        self.delete_button = tk.Button(root, text="Delete Selected Tasks", command=self.delete_selected_tasks, font=('Arial', 12), bg='#F44336', fg='white', width=20)
        self.delete_button.pack(pady=5, fill=tk.X, padx=10)

        # Clear all tasks
        self.clear_all_button = tk.Button(root, text="Clear All Tasks", command=self.clear_all_todos, font=('Arial', 12), bg='#FF5722', fg='white', width=20)
        self.clear_all_button.pack(pady=5, fill=tk.X, padx=10)

    def update_listbox(self):
        for widget in self.listbox_inner_frame.winfo_children():
            widget.destroy()

        for idx, todo in enumerate(self.todos):
            todo_text = todo['text']
            completed = todo.get('completed', False)
            selected = todo.get('selected', False)

            bg_color = '#ffffff' if not selected else '#b3e5fc'  # Light blue for selected tasks

            row_frame = tk.Frame(self.listbox_inner_frame, bg='#e0e0e0')
            row_frame.pack(pady=5, fill=tk.X)

            label_text = todo_text
            if completed:
                label_text = f"{label_text} (✓)"  # Text for completed tasks

            label = tk.Label(row_frame, text=label_text, bg=bg_color, font=('Arial', 12), padx=10, pady=5, anchor='w', bd=1, relief=tk.RAISED)
            if completed:
                label.config(font=('Arial', 12, 'overstrike'))
            label.pack(side=tk.LEFT, fill=tk.X, pady=2, padx=5)

            button_frame = tk.Frame(row_frame, bg='#e0e0e0')
            button_frame.pack(side=tk.RIGHT, padx=5)

            select_button = tk.Button(button_frame, text="+", command=lambda idx=idx: self.select_task(idx), font=('Arial', 12, 'bold'), bg='#FFC107', fg='black', width=2, height=1)
            select_button.pack(side=tk.LEFT, padx=2)

            complete_button = tk.Button(button_frame, text="✓", command=lambda idx=idx: self.toggle_task(idx), font=('Arial', 12, 'bold'), bg='#2196F3', fg='white', width=2, height=1)
            complete_button.pack(side=tk.LEFT, padx=2)

            delete_button = tk.Button(button_frame, text="X", command=lambda idx=idx: self.delete_task(idx), font=('Arial', 12, 'bold'), bg='#F44336', fg='white', width=2, height=1)
            delete_button.pack(side=tk.LEFT, padx=2)

    def add_todo_event(self, event):
        self.add_todo()

    def add_todo(self):
        todo_text = self.entry.get().strip()
        if todo_text:
            self.todos.append({'text': todo_text, 'selected': False})
            self.save_todos()
            self.update_listbox()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, "Enter task")
        else:
            messagebox.showwarning("Warning", "Task must be entered.")

    def toggle_task(self, idx):
        """Toggles the completion status of a task."""
        self.todos[idx]['completed'] = not self.todos[idx].get('completed', False)
        self.save_todos()
        self.update_listbox()

    def delete_task(self, idx):
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this task?"):
            del self.todos[idx]
            self.save_todos()
            self.update_listbox()

    def delete_selected_tasks(self):
        selected_indices = [i for i, todo in enumerate(self.todos) if todo.get('selected', False)]
        if not selected_indices:
            messagebox.showwarning("Warning", "No tasks selected.")
            return

        if messagebox.askyesno("Confirmation", f"Are you sure you want to delete {len(selected_indices)} selected task(s)?"):
            for idx in sorted(selected_indices, reverse=True):
                del self.todos[idx]
            self.save_todos()
            self.update_listbox()

    def select_task(self, idx):
        """This function toggles the selection state of the task."""
        self.todos[idx]['selected'] = not self.todos[idx].get('selected', False)
        self.save_todos()
        self.update_listbox()

    def clear_all_todos(self):
        self.todos.clear()
        self.save_todos()
        self.update_listbox()

    def save_todos(self):
        with open(TODO_FILE, 'w') as f:
            json.dump(self.todos, f)

    def load_todos(self):
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, 'r') as f:
                return json.load(f)
        return []

    def clear_placeholder(self, event):
        if self.entry.get() == "Enter task":
            self.entry.delete(0, tk.END)

    def set_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, "Enter task")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
