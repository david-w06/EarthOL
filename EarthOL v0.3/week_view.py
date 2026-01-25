import customtkinter as ctk
import tkinter as tk
from datetime import datetime, timedelta, date
import theme

class WeekView(ctk.CTkFrame):
    def __init__(self, master, task_manager):
        super().__init__(master, fg_color="transparent")
        self.task_manager = task_manager
        
        # State
        self.current_date = date.today()
        self.start_of_week = self.get_start_of_week(self.current_date)
        
        # Constants
        self.hour_height = 60
        self.day_width = 150
        self.start_hour = 6
        self.end_hour = 24
        self.header_height = 50
        self.left_margin_width = 60
        
        self.colors = {
            "School Work": "#3b82f6",
            "Self-Study-STEM": "#8b5cf6",
            "Self-Study-Humanities": "#ec4899",
            "Workout": "#ef4444",
            "Combat Training": "#f97316",
            "Looks": "#f59e0b",
            "Practice Music": "#10b981",
            "Practice Arts": "#14b8a6",
            "Play Sports": "#06b6d4",
            "Others": "#64748b"
        }

        self.create_ui()

    def get_start_of_week(self, d):
        # Monday is 0
        return d - timedelta(days=d.weekday())

    def create_ui(self):
        # Header controls
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.btn_prev = ctk.CTkButton(self.header_frame, text="<", width=40, command=self.prev_week)
        self.btn_prev.pack(side="left", padx=5)

        self.btn_today = ctk.CTkButton(self.header_frame, text="Today", width=60, command=self.go_today)
        self.btn_today.pack(side="left", padx=5)

        self.btn_next = ctk.CTkButton(self.header_frame, text=">", width=40, command=self.next_week)
        self.btn_next.pack(side="left", padx=5)

        self.date_label = ctk.CTkLabel(self.header_frame, text="", font=("Arial", 16, "bold"))
        self.date_label.pack(side="left", padx=20)
        
        # Canvas Container (Scrollable) inside a frame
        self.canvas_frame = ctk.CTkFrame(self, corner_radius=0)
        self.canvas_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        self.v_scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="vertical")
        self.v_scrollbar.pack(side="right", fill="y")
        
        self.h_scrollbar = ctk.CTkScrollbar(self.canvas_frame, orientation="horizontal")
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg=theme.BG_MAIN,
            highlightthickness=0,
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)

        self.v_scrollbar.configure(command=self.canvas.yview)
        self.h_scrollbar.configure(command=self.canvas.xview)

        #Fast Travel
        self.jump_label = ctk.CTkLabel(self.header_frame, text="Jump to...", font=("Arial", 16, "bold"))
        self.jump_label.pack(side="left", padx=(20, 5))

        self.jump_entry = ctk.CTkEntry(self.header_frame, width=100, placeholder_text="YYYY-MM")
        current_val = date.today().strftime("%Y-%m")
        self.jump_entry.insert(0, current_val)
        self.jump_entry.pack(side="left", padx=5)

        self.btn_jump = ctk.CTkButton(self.header_frame, text="Go", width=80, command=self.handle_jump)
        self.btn_jump.pack(side="left", padx=5)

    def handle_jump(self):
        input_data = self.jump_entry.get().strip()

        if input_data:
            try:
                year, month = map(int, input_data.split("-"))
                self.fast_travel(year, month)
            except (ValueError, AttributeError):
                pass

    def fast_travel(self, year, month):
        # Logic remains the same
        target_date = date(year, month, 1)
        self.start_of_week = self.get_start_of_week(target_date)
        self.refresh()


        # Bind events
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.refresh()

    def on_resize(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def prev_week(self):
        self.start_of_week -= timedelta(days=7)
        self.refresh()

    def next_week(self):
        self.start_of_week += timedelta(days=7)
        self.refresh()

    def go_today(self):
        self.start_of_week = self.get_start_of_week(date.today())
        self.refresh()

    def refresh(self):
        self.update_header()
        self.draw_grid()
        self.draw_tasks()
        
    def update_header(self):
        end_of_week = self.start_of_week + timedelta(days=6)
        start_str = self.start_of_week.strftime("%b %d")
        end_str = end_of_week.strftime("%b %d")
        year_str = self.start_of_week.strftime("%Y")
        self.date_label.configure(text=f"{start_str} - {end_str}, {year_str}")

    def draw_grid(self):
        self.canvas.delete("all")
        
        # Draw Time Labels (Left Column)
        total_hours = self.end_hour - self.start_hour
        
        # Headers (Days)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            current_day_date = self.start_of_week + timedelta(days=i)
            # Highlight today
            color = "#ffffff"
            if current_day_date == date.today():
                color = "#2a85ff"
                
            x = self.left_margin_width + i * self.day_width
            title = f"{day} {current_day_date.day}"
            
            self.canvas.create_text(
                x + self.day_width / 2, 
                self.header_height / 2, 
                text=title, 
                fill=color, 
                font=("Arial", 12, "bold")
            )
            
            # Vertical lines
            self.canvas.create_line(
                x - 1, 0,
                x - 1, self.header_height + total_hours * self.hour_height,
                fill="#ffffff",
                width=1)


        # Draw Hours and Horizontal Lines, take care of the top edge case
        self.canvas.create_line(
            self.left_margin_width,
            self.header_height,
            self.left_margin_width + 7 * self.day_width,
            self.header_height,
            fill="#ffffff",
            width=1
        )

        for i in range(total_hours + 1):
            y = self.header_height + i * self.hour_height
            hour_label = f"{self.start_hour + i:02d}:00"
            
            # Time label
            self.canvas.create_text(
                self.left_margin_width / 2,
                y,
                text=hour_label,
                fill="#ffffff",
                font=("Arial", 10)
            )
            
            # Horizontal line
            self.canvas.create_line(
                self.left_margin_width, y, 
                self.left_margin_width + 7 * self.day_width, y,
                fill="#ffffff", width=1
            )

        # Set scroll region
        total_width = self.left_margin_width + 7 * self.day_width
        total_height = self.header_height + total_hours * self.hour_height
        self.canvas.configure(scrollregion=(0, 0, total_width, total_height))

    def draw_tasks(self):
        for task in self.task_manager.tasks:
            if not task.start_time:
                continue
                
            # Check if task is in current week
            task_date = task.start_time.date()
            if not (self.start_of_week <= task_date < self.start_of_week + timedelta(days=7)):
                continue
                
            # Check if task is within visible hours
            start_hour = task.start_time.hour + task.start_time.minute / 60
            if start_hour < self.start_hour or start_hour >= self.end_hour:
                continue # simplified logic, skips tasks starting outside range

            # Calculate geometry
            day_index = (task_date - self.start_of_week).days
            
            x1 = self.left_margin_width + day_index * self.day_width + 2
            x2 = x1 + self.day_width - 4
            
            y1 = self.header_height + (start_hour - self.start_hour) * self.hour_height
            height = (task.duration / 60) * self.hour_height
            y2 = y1 + height
            
            # Defaults
            bg_color = self.colors.get(task.category, "#444444")
            
            # Draw rectangle
            rect = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=bg_color,
                outline="",
                tags="task"
            )
            
            # Draw text
            text_y = y1 + 5
            self.canvas.create_text(
                x1 + 5, text_y,
                text=task.name,
                anchor="nw",
                fill="white",
                font=("Arial", 10, "bold"),
                width=self.day_width - 10
            )
            
            self.canvas.create_text(
                x1 + 5, text_y + 15,
                text=f"{task.start_time.strftime('%H:%M')} ({task.duration}m)",
                anchor="nw",
                fill="white",
                font=("Arial", 9),
            )

