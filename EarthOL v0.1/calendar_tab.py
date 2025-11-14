import calendar
import customtkinter as ctk
from datetime import date

from datetime import datetime
import customtkinter as ctk

class CalendarTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.events = {}

        self.create_ui()

    def create_ui(self):
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16)

        # Title (Month + Year)
        self.title_label = ctk.CTkLabel(
            self.stats_frame,
            text=f"{datetime.now().strftime("%B")} {self.current_year}",
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(pady=10)

        # Frame for the calendar grid
        self.grid_frame = ctk.CTkFrame(self.stats_frame)
        self.grid_frame.pack()

        self.draw_calendar()

    def draw_calendar(self):
        # Clear old grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Weekday headers
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            ctk.CTkLabel(self.grid_frame, text=day).grid(row=0, column=i, padx=5, pady=5)

        # Calendar grid
        cal = calendar.monthcalendar(self.current_year, self.current_month)

        for row_idx, week in enumerate(cal, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    text = ""
                else:
                    text = str(day)

                # Check if this day has events
                key = (self.current_year, self.current_month, day)
                if key in self.events and self.events[key]:
                    # Highlight days with events (e.g., blue background)
                    fg_color = "#2a85ff"  # text color
                    btn_color = "#1f1f1f"  # normal button background
                else:
                    fg_color = "white"
                    btn_color = "#111111"

                label = ctk.CTkButton(
                    self.grid_frame,
                    text=text,
                    width=40,
                    height=40,
                    corner_radius=8,
                    fg_color=btn_color,
                    text_color=fg_color,
                    command=lambda d=day: self.day_selected(d)
                )
                label.grid(row=row_idx, column=col_idx, padx=5, pady=5)

    def day_selected(self, day):
        if day == 0:
            return

        key = (self.current_year, self.current_month, day)
        events = self.events.get(key, [])

        # Create popup
        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Events for {self.current_year}-{self.current_month}-{day}")
        popup.geometry("300x200")

        title = ctk.CTkLabel(popup, text=f"Events on {self.current_year}-{self.current_month}-{day}",
                             font=("Arial", 16, "bold"))
        title.pack(pady=10)

        if not events:
            ctk.CTkLabel(popup, text="No events").pack(pady=10)
        else:
            for evt in events:
                ctk.CTkLabel(popup, text=f"• {evt}", anchor="w", justify="left").pack(padx=10, pady=2)

    def show(self):
        self.stats_frame.pack(pady=10, padx=16, fill="both", expand=True)

    def hide(self):
        self.stats_frame.pack_forget()

    def refresh(self):
        pass

    def add_event_today(self, text, exp):
        key = (self.current_year, self.current_month, date.today().day)

        if key not in self.events:
            self.events[key] = []

        self.events[key].append(f"{text}: Gained {int(exp)} exp.")
        self.draw_calendar()






