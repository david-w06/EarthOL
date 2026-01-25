from tkinter import messagebox, simpledialog
from task_manager import TaskManager
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from week_view import WeekView
import theme

class TasksTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root
        self.manager = TaskManager("tasks.json")
        self.calendar_tab = main_app.calendar_tab

        self.create_ui()

    def create_ui(self):
        """Create all UI elements for tasks tab"""
        # Main frame
        self.tasks_frame = ctk.CTkFrame(self.root, corner_radius=16, fg_color="transparent")

        # --- List View Container ---
        self.list_container = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        self.list_container.pack(fill="both", expand=True)

        # Title
        # title_label = ctk.CTkLabel(
        #     self.list_container,
        #     text="📋 Task Manager",
        #     font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
        #     text_color=theme.TEXT_PRIMARY
        # )
        # title_label.pack(pady=(10, 5))

        # Header / Control Bar
        control_bar = ctk.CTkFrame(self.list_container, fg_color=theme.BG_CONTAINER, height=60, corner_radius=12)
        control_bar.pack(fill="x", pady=(0, 15), padx=5)

        ctk.CTkLabel(control_bar, text="My Tasks", font=ctk.CTkFont(size=20, weight="bold"), text_color=theme.TEXT_PRIMARY).pack(side="left", padx=20, pady=10)

        # Action buttons
        
        def make_action_btn(text, cmd, color=theme.BTN_BG, hover=theme.BTN_HOVER):
             return ctk.CTkButton(
                control_bar, 
                text=text, 
                command=cmd, 
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=color, 
                hover_color=hover,
                height=32,
                corner_radius=8
            )

        make_action_btn("📅 Calendar View", self.show_calendar_view).pack(side="right", padx=10)
        make_action_btn("➕ New Task", self.open_add_task_window, color=theme.ACCENT_BLUE).pack(side="right", padx=5)
        
        # Scrollable Task List
        self.task_scroll_frame = ctk.CTkScrollableFrame(
            self.list_container,
            fg_color="transparent",
            corner_radius=0
        )
        self.task_scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)


        # --- Calendar View Container ---
        self.calendar_container = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        # Hidden by default

        # Back button for calendar
        ctk.CTkButton(
            self.calendar_container, 
            text="⬅ Back to List", 
            command=self.show_list_view,
            fg_color=theme.BTN_BG,
            hover_color=theme.BTN_HOVER
        ).pack(anchor="w", padx=10, pady=10)

        self.week_view = WeekView(self.calendar_container, self.manager)
        self.week_view.pack(fill="both", expand=True)

    def show(self):
        """Display the tasks tab"""
        self.tasks_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.refresh()

    def hide(self):
        """Hide the tasks tab"""
        self.tasks_frame.pack_forget()

    def refresh(self):
        """Refresh the task list display"""
        # Clear existing
        for widget in self.task_scroll_frame.winfo_children():
            widget.destroy()

        if not self.manager.tasks:
            ctk.CTkLabel(
                self.task_scroll_frame, 
                text="No tasks found. Click 'New Task' to get started!",
                text_color=theme.TEXT_MUTED,
                font=ctk.CTkFont(size=16)
            ).pack(pady=40)
        else:
            for task in self.manager.tasks:
                self.render_task_row(task)

    def render_task_row(self, task):
        """Render a single task row"""
        row = ctk.CTkFrame(self.task_scroll_frame, fg_color=theme.BG_CARD, corner_radius=10, border_width=1, border_color=theme.BORDER_NORMAL)
        row.pack(fill="x", pady=6, padx=5)

        # Status Indicator (Left Border equivalent)
        status_color = theme.ACCENT_GREEN if task.completed else theme.ACCENT_BLUE
        
        # Checkbox / Done Button
        done_btn = ctk.CTkButton(
            row,
            text="✔" if task.completed else "",
            width=32,
            height=32,
            corner_radius=8,
            fg_color=theme.ACCENT_GREEN if task.completed else theme.BTN_BG,
            hover_color=theme.ACCENT_GREEN,
            border_width=1 if not task.completed else 0,
            border_color=theme.BORDER_HIGHLIGHT,
            command=lambda t=task: self.mark_task_done(t)
        )
        done_btn.pack(side="left", padx=(15, 15), pady=15)

        # Task Info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=10)

        name_font = ctk.CTkFont(size=16, weight="bold", overstrike=task.completed)
        name_color = theme.TEXT_MUTED if task.completed else theme.TEXT_PRIMARY
        
        ctk.CTkLabel(info_frame, text=task.name, font=name_font, text_color=name_color, anchor="w").pack(fill="x")
        
        details_text = f"{task.category}  •  {task.duration} min"
        if task.start_time:
             details_text += f"  •  {task.start_time}"
            
        ctk.CTkLabel(info_frame, text=details_text, font=ctk.CTkFont(size=12), text_color=theme.TEXT_MUTED, anchor="w").pack(fill="x")

        # Delete Button
        ctk.CTkButton(
            row,
            text="🗑",
            width=32,
            height=32,
            fg_color="transparent",
            hover_color=theme.ACCENT_RED,
            text_color=theme.TEXT_SECONDARY,
            font=ctk.CTkFont(size=16),
            command=lambda t=task: self.delete_task_object(t)
        ).pack(side="right", padx=15)


    def open_add_task_window(self):
        """Open popup to add new task"""
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("Add New Task")
        add_window.geometry("420x500")
        add_window.configure(fg_color=theme.BG_MAIN)
        add_window.grab_set()

        wrap = ctk.CTkFrame(add_window, corner_radius=12, fg_color=theme.BG_CONTAINER)
        wrap.pack(fill="both", expand=True, padx=20, pady=20)

        def add_field(label_text, placeholder):
            ctk.CTkLabel(wrap, text=label_text, text_color=theme.TEXT_PRIMARY).pack(anchor="w", pady=(10, 2))
            entry = ctk.CTkEntry(wrap, width=340, placeholder_text=placeholder, fg_color=theme.BTN_BG, border_color=theme.BORDER_NORMAL)
            entry.pack(pady=2)
            return entry

        # Task name
        name_entry = add_field("Task Name:", "e.g., Math Assignment 1")

        # Category
        ctk.CTkLabel(wrap, text="Category:", text_color=theme.TEXT_PRIMARY).pack(anchor="w", pady=(10, 2))
        category_options = [
            "School Work", "Self-Study-STEM", "Self-Study-Humanities", "Workout",
            "Combat Training", "Looks", "Practice Music", "Practice Arts",
            "Play Sports", "Others"
        ]
        category_var = ctk.StringVar(value=category_options[0])
        category_dropdown = ctk.CTkComboBox(wrap, variable=category_var, values=category_options, width=340, fg_color=theme.BTN_BG, border_color=theme.BORDER_NORMAL, button_color=theme.ACCENT_BLUE)
        category_dropdown.pack(pady=2)

        # Scheduled time
        time_entry = add_field("Scheduled Time:", "e.g., 2025-11-05 15:00 or leave blank")

        # Duration
        duration_entry = add_field("Duration in minutes:", "e.g., 60")

        # Note
        note_entry = add_field("Note:", "optional")

        def save_and_close():
            name = name_entry.get().strip()
            duration_str = duration_entry.get().strip()

            if not name:
                messagebox.showwarning("Warning", "Task name cannot be empty.")
                return

            if self.manager.get_task(name):
                messagebox.showwarning("Warning", f"'{name}' already exist.")
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
            note = note_entry.get().strip() or ""

            raw_time = time_entry.get().strip()

            if raw_time:
                try:
                    start_time = datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
                except ValueError:
                    messagebox.showerror("Invalid Time Format", "Use YYYY-MM-DD HH:MM")
                    return
            else:
                start_time = None

            self.manager.add_task(name, start_time, category, duration, note)
            self.refresh()
            add_window.destroy()

        ctk.CTkButton(
            wrap, 
            text="Add Task", 
            command=save_and_close, 
            width=340, 
            height=40,
            fg_color=theme.ACCENT_BLUE,
            hover_color="#0ea5e9", # a slightly darker blue
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=30)
    
    # NEW: Direct task object manipulation instead of listbox selection
    def mark_task_done(self, task):
        if task.completed:
            messagebox.showinfo("Info", f"'{task.name}' is already done.")
            return

        self.calendar_tab.add_event_today(task.name, 0)
        self.manager.mark_done(task.name)

        player = self.main_app.get_player()
        category = task.category

        if category == "School Work":
            self.handle_school_work_xp(task, player)
        else:
            self.ask_focus_rating(task, category, player)

        self.refresh()
        self.main_app.refresh_all()

    # Need to keep the legacy method signatures if they are called dynamically, but usually we just replace them.
    # The old mark_done depended on listbox selection. We can remove it or keep it as a stub.
    # I'll simply strictly implement what's needed.

    def delete_task_object(self, task):
        if messagebox.askyesno("Confirm", f"Delete '{task.name}'?"):
            self.manager.delete_task(task.name)
            self.refresh()

    def handle_school_work_xp(self, task, player):
        # --- Grade popup ---
        grade = self.ask_float_popup(
            title="Enter Grade",
            prompt=f"Enter your grade (0–100):\n'{task.name}'",
            min_val=0,
            max_val=100
        )
        if grade is None:
            return

        # --- Target popup ---
        target = self.ask_float_popup(
            title="Target Grade",
            prompt="Enter your target grade (0–100):",
            min_val=0,
            max_val=100
        )
        if target is None:
            return

        # --- Weight popup ---
        weight = self.ask_float_popup(
            title="Assignment Weight",
            prompt="Enter assignment weight (0–1):",
            min_val=0,
            max_val=1
        )
        if weight is None:
            return

        disc = player.discipline if hasattr(player, "discipline") else 0
        base = int(task.duration)

        raw_xp = (
                base
                * (grade / 100)
                * ((grade - target) / 5)
                * (1 + disc)
                * weight)
        #right now for the formula, if you are not getting above the target there is no xp, maybe change that?
        if raw_xp < 0:
            raw_xp = 0

        player.add_experience(raw_xp)
        player.intelligence += raw_xp * 0.4
        player.knowledge += raw_xp * 0.6

        messagebox.showinfo("XP Gained", f"You earned {raw_xp:.1f} XP from {task.category}.")
        self.calendar_tab.add_event_today(task.name, raw_xp)

    def ask_focus_rating(self, task, category, player):
        """Ask for focus rating and award XP"""
        popup = ctk.CTkToplevel(self.root)
        popup.title("Rate Your Focus")
        popup.geometry("320x260")
        popup.configure(fg_color=theme.BG_MAIN)
        popup.grab_set()
        
        frame = ctk.CTkFrame(popup, fg_color=theme.BG_CONTAINER, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(frame, text=f"How focused were you on\n'{task.name}'?", font=ctk.CTkFont(size=16)).pack(pady=15)

        selected = tk.IntVar(value=0)
        
        # Custom radio buttons or just simple buttons. Let's use simple buttons for clearer UX.
        
        def rate(i):
            popup.destroy()
            self.calculate_xp(task, category, player, i)
            
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        for i in range(1, 6):
            ctk.CTkButton(
                btn_frame, 
                text=str(i), 
                width=40, 
                height=40,
                corner_radius=20,
                fg_color=theme.BTN_BG,
                hover_color=theme.ACCENT_BLUE,
                command=lambda val=i: rate(val)
            ).pack(side="left", padx=4)
            
        ctk.CTkLabel(frame, text="1 (Low)  -  5 (High)", text_color=theme.TEXT_MUTED).pack()


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

        player.save()

        messagebox.showinfo("XP Gained", f"You earned {raw_xp:.1f} XP from {category}.")
        self.calendar_tab.add_event_today(task.name, raw_xp)

    def show_calendar_view(self):
        """Switch to calendar view"""
        self.list_container.pack_forget()
        self.calendar_container.pack(fill="both", expand=True)
        self.week_view.refresh()

    def show_list_view(self):
        """Switch to list view"""
        self.calendar_container.pack_forget()
        self.list_container.pack(fill="both", expand=True)
        self.refresh()

    def ask_float_popup(self, title, prompt, min_val, max_val):
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("320x260")
        popup.configure(fg_color=theme.BG_MAIN)
        popup.grab_set()

        frame = ctk.CTkFrame(popup, fg_color=theme.BG_CONTAINER, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(
            frame,
            text=prompt,
            font=ctk.CTkFont(size=16),
            wraplength=260
        ).pack(pady=15)

        value = ctk.StringVar()
        entry = ctk.CTkEntry(frame, textvariable=value)
        entry.pack(pady=10)

        error_label = ctk.CTkLabel(frame, text="", text_color="red")
        error_label.pack(pady=5)

        result = {"value": None}

        def submit():
            try:
                v = float(value.get())
                if not (min_val <= v <= max_val):
                    raise ValueError
                result["value"] = v
                popup.destroy()
            except ValueError:
                error_label.configure(
                    text=f"Enter a number between {min_val} and {max_val}"
                )

        ctk.CTkButton(frame, text="Submit", command=submit).pack(pady=10)

        popup.wait_window()
        return result["value"]
