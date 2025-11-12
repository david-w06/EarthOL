import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
from task_manager import TaskManager


class TasksTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root
        self.manager = TaskManager("tasks.json")

        self.create_ui()

    def create_ui(self):
        """Create all UI elements for tasks tab"""
        # Main frame
        self.tasks_frame = ctk.CTkFrame(self.root, corner_radius=16)

        # Title
        title_label = ctk.CTkLabel(
            self.tasks_frame,
            text="📋 Task Manager",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Button frame
        button_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        # Action buttons
        ctk.CTkButton(button_frame, text="➕ Add Task", command=self.open_add_task_window).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="✅ Mark Done", command=self.mark_done).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Delete", command=self.delete_task).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🔄 Refresh", command=self.refresh).pack(side="left", padx=5)

        # Task list frame
        listbox_frame = ctk.CTkFrame(self.tasks_frame)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Listbox label
        ctk.CTkLabel(listbox_frame, text="Your Tasks:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 0))

        self.task_listbox = tk.Listbox(
            listbox_frame,
            width=90,
            height=18,
            bg="#111111",
            fg="white",
            selectforeground="white",
            highlightbackground="#111111",
            borderwidth=0,
            selectbackground="#2a85ff",
            font=("Arial", 10)
        )
        self.task_listbox.pack(fill="both", expand=True, padx=6, pady=6)

    def show(self):
        """Display the tasks tab"""
        self.tasks_frame.pack(fill="both", expand=True, padx=16, pady=16)
        self.refresh()

    def hide(self):
        """Hide the tasks tab"""
        self.tasks_frame.pack_forget()

    def refresh(self):
        """Refresh the task list display"""
        self.task_listbox.delete(0, tk.END)
        if not self.manager.tasks:
            self.task_listbox.insert(tk.END, "No tasks found. Click 'Add Task' to get started!")
        else:
            for task in self.manager.tasks:
                self.task_listbox.insert(tk.END, str(task))

    # ... (rest of the methods remain the same as previous implementation)
    def open_add_task_window(self):
        """Open popup to add new task"""
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Add New Task")
        add_window.geometry("380x450")
        add_window.grab_set()

        wrap = ctk.CTkFrame(add_window, corner_radius=12)
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        # Task name
        ctk.CTkLabel(wrap, text="Task Name:").pack(anchor="w", pady=(6, 2))
        name_entry = ctk.CTkEntry(wrap, width=300, placeholder_text="e.g., Math Assignment 1")
        name_entry.pack(pady=4)

        # Category
        ctk.CTkLabel(wrap, text="Category:").pack(anchor="w", pady=(8, 2))
        category_options = [
            "School Work", "Self-Study-STEM", "Self-Study-Humanities", "Workout",
            "Combat Training", "Looks", "Practice Music", "Practice Arts",
            "Play Sports", "Others"
        ]
        category_var = ctk.StringVar(value=category_options[0])
        category_dropdown = ctk.CTkComboBox(wrap, variable=category_var, values=category_options, width=300)
        category_dropdown.pack(pady=4)

        # Scheduled time
        ctk.CTkLabel(wrap, text="Scheduled Time:").pack(anchor="w", pady=(8, 2))
        time_entry = ctk.CTkEntry(wrap, width=300, placeholder_text="e.g., 2025-11-05 15:00 or leave blank")
        time_entry.pack(pady=4)

        # Duration
        ctk.CTkLabel(wrap, text="Duration in minutes:").pack(anchor="w", pady=(8, 2))
        duration_entry = ctk.CTkEntry(wrap, width=300, placeholder_text="e.g., 60")
        duration_entry.pack(pady=4)

        # Note
        ctk.CTkLabel(wrap, text="Note:").pack(anchor="w", pady=(8, 2))
        note_entry = ctk.CTkEntry(wrap, width=300, placeholder_text="optional")
        note_entry.pack(pady=4)

        def save_and_close():
            name = name_entry.get().strip()
            duration_str = duration_entry.get().strip()

            if not name:
                messagebox.showwarning("Warning", "Task name cannot be empty.")
                return

            if not duration_str:
                messagebox.showwarning("Warning", "Task duration must be set.")
                return

            try:
                duration = int(duration_str)
            except ValueError:
                messagebox.showerror("Invalid Input", "Duration must be a number.")
                return

            category = category_var.get()
            scheduled_time = time_entry.get().strip() or "No time"
            note = note_entry.get().strip() or ""

            self.manager.add_task(name, scheduled_time, category, duration, note)
            self.refresh()
            add_window.destroy()

        ctk.CTkButton(wrap, text="Add Task", command=save_and_close).pack(pady=12)

    def mark_done(self):
        """Mark selected task as done and award XP"""
        try:
            selection = self.task_listbox.get(self.task_listbox.curselection())
            name = selection.split(" | ")[0].replace("✅", "").replace("⬜", "").strip()
            task = self.manager.get_task(name)

            if not task:
                messagebox.showerror("Error", "Task not found.")
                return

            self.manager.mark_done(name)

            # Get player from main app to award XP
            player = self.main_app.get_player()
            category = task.category

            if category == "School Work":
                self.handle_school_work_xp(task, player)
            else:
                self.ask_focus_rating(task, category, player)

            self.refresh()
            self.main_app.refresh_all()  # Update stats tab

        except tk.TclError:
            messagebox.showwarning("Warning", "Please select a task to mark as done.")
        except Exception as e:
            messagebox.showerror("Error", f"Error marking task done: {e}")

    def handle_school_work_xp(self, task, player):
        """Handle XP calculation for school work"""
        grade = simpledialog.askfloat("Grade", "Enter your grade (0–100):",
                                      parent=self.root, minvalue=0, maxvalue=100)
        target = simpledialog.askfloat("Target", "Enter your target grade (0–100):",
                                       parent=self.root, minvalue=0, maxvalue=100)
        weight = simpledialog.askfloat("Weight", "Enter assignment weight (0–1):",
                                       parent=self.root, minvalue=0, maxvalue=1)

        disc = player.discipline if hasattr(player, "discipline") else 0
        base = int(task.duration)
        raw_xp = base * (grade / 100) * ((grade - target) / 5) * (1 + disc) * weight

        if raw_xp < 0:
            raw_xp = 0

        player.add_experience(raw_xp)
        player.intelligence += raw_xp * 0.4
        player.knowledge += raw_xp * 0.6

        messagebox.showinfo("XP Gained", f"You earned {raw_xp:.1f} XP from {task.category}.")

    def ask_focus_rating(self, task, category, player):
        """Ask for focus rating and award XP"""
        popup = tk.Toplevel(self.root)
        popup.title("Rate Your Focus")
        popup.geometry("250x200")
        popup.grab_set()

        tk.Label(popup, text=f"How focused were you on '{task.name}'?", wraplength=200).pack(pady=10)

        selected = tk.IntVar(value=0)
        for i in range(1, 5):
            tk.Radiobutton(popup, text=f"{i} - {'⭐' * i}", variable=selected, value=i).pack(anchor="w")

        def submit_rating():
            focus_rating = selected.get()
            if focus_rating == 0:
                messagebox.showwarning("Missing", "Please select a focus level.")
                return

            popup.destroy()
            self.calculate_xp(task, category, player, focus_rating)

        tk.Button(popup, text="Submit", command=submit_rating).pack(pady=10)

    def calculate_xp(self, task, category, player, focus_rating):
        """Calculate and award XP based on category"""
        raw_xp = task.duration * (1 + 0.08 * focus_rating ** 2)
        player.add_experience(raw_xp)

        # Attribute distribution
        if category == "Self-Study-STEM":
            player.intelligence += raw_xp * 0.6
            player.knowledge += raw_xp * 0.2
            player.discipline += raw_xp * 0.1
        elif category == "Self-Study-Humanities":
            player.intelligence += raw_xp * 0.1
            player.knowledge += raw_xp * 0.5
            player.SE += raw_xp * 0.1
            player.discipline += raw_xp * 0.3
        elif category == "Workout":
            player.athleticism += raw_xp * 0.6
            player.combat += raw_xp * 0.1
            player.discipline += raw_xp * 0.3
        elif category == "Combat Training":
            player.athleticism += raw_xp * 0.5
            player.combat += raw_xp * 0.4
            player.discipline += raw_xp * 0.1
        elif category == "Looks":
            player.discipline += raw_xp * 0.3
            player.looks += raw_xp * 0.4
        elif category == "Practice Music":
            player.artistry += raw_xp * 0.6
            player.discipline += raw_xp * 0.2
        elif category == "Practice Arts":
            player.artistry += raw_xp * 0.7
            player.discipline += raw_xp * 0.2
        elif category == "Play Sports":
            player.athleticism += raw_xp * 0.5
            player.SE += raw_xp * 0.3
        else:  # Others
            player.discipline += raw_xp * 0.3

        messagebox.showinfo("XP Gained", f"You earned {raw_xp:.1f} XP from {category}.")

    def delete_task(self):
        """Delete selected task"""
        try:
            selection = self.task_listbox.get(self.task_listbox.curselection())
            name = selection.split(" | ")[0].replace("✅", "").replace("⬜", "").strip()
            self.manager.delete_task(name)
            self.refresh()
        except tk.TclError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def delete_all_tasks(self):
        """Delete all tasks"""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all tasks?"):
            self.manager.tasks = []
            self.manager.save_tasks()
            self.refresh()