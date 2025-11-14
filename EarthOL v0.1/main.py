import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from home import HomeTab
from ttask import TasksTab
from stats import StatsTab
from journal import JournalTab
from calendar_tab import CalendarTab


class TaskManagerApp:
    def __init__(self):
        # --- Theme ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Window ---
        self.root = ctk.CTk()
        self.root.title("Earth Online")


        #proportional screen for the user instead of a locked small screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.65)
        window_height = int(screen_height * 0.65)
        self.root.geometry(f"{window_width}x{window_height}")
        # self.root.resizable(False, False) #lock window size

        # Create navigation frame (always visible except on home)
        self.nav_frame = ctk.CTkFrame(self.root, height=50, corner_radius=0)

        # Initialize tab classes
        self.home_tab = HomeTab(self)
        self.calendar_tab = CalendarTab(self)
        self.tasks_tab = TasksTab(self)
        self.stats_tab = StatsTab(self)
        self.journal_tab = JournalTab(self)
        #.... add other tabs

        # Current tab tracking
        self.current_tab = None


        # Show home by default
        self.show_tab("home")

    def create_navigation(self):
        """Create the top navigation bar"""
        # Clear existing navigation
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        # Navigation buttons
        nav_buttons_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        nav_buttons_frame.pack(pady=10)


        ctk.CTkButton(
            nav_buttons_frame,
            text="Home",
            width=120,
            command=lambda: self.show_tab("home")
        ).pack(side="left", padx=5)

        # Other tabs
        ctk.CTkButton(
            nav_buttons_frame,
            text="Tasks",
            width=120,
            command=lambda: self.show_tab("tasks")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            nav_buttons_frame,
            text="Stats",
            width=120,
            command=lambda: self.show_tab("stats")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            nav_buttons_frame,
            text="Journal",
            width=120,
            command=lambda: self.show_tab("journal")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            nav_buttons_frame,
            text="Calendar",
            width=120,
            command=lambda: self.show_tab("calendar")
        ).pack(side="left", padx=5)

    def show_tab(self, tab_name):
        """Hide current tab and show the requested tab"""
        # Hide current tab if exists
        if self.current_tab:
            self.current_tab.hide()

        # Show navigation for all tabs except home
        if tab_name == "home":
            self.nav_frame.pack_forget()
        else:
            self.nav_frame.pack(fill="x", padx=0, pady=0)
            self.create_navigation()

        # Show new tab
        if tab_name == "home":
            self.current_tab = self.home_tab
        elif tab_name == "tasks":
            self.current_tab = self.tasks_tab
        elif tab_name == "stats":
            self.current_tab = self.stats_tab
        elif tab_name == "journal":
            self.current_tab = self.journal_tab
        elif tab_name == "calendar":
            self.current_tab = self.calendar_tab

        self.current_tab.show()

    def get_manager(self):
        """Get task manager from tasks tab"""
        return self.tasks_tab.manager

    def get_player(self):
        """Get player from stats tab"""
        return self.stats_tab.player

    def refresh_all(self):
        """Refresh all tabs when data changes"""
        self.tasks_tab.refresh()
        self.stats_tab.refresh()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()