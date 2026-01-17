import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from home import HomeTab
from ttask import TasksTab
from stats import StatsTab
from journal import JournalTab
from calendar_tab import CalendarTab
from note import NotesTab
from player_profile import Player
from introscreen import IntroScreen

import os
import json


# ----------------- EXP SYSTEM ----------------- #
class SegmentedExpBar(ctk.CTkFrame):
    def __init__(self, master, exp_value, exp_level, width=340, height=24,
                 gap=1, corner_radius=3, empty_color="#171717"):
        super().__init__(master, fg_color="transparent")

        exp_percent = round((exp_value / exp_level) * 100) if exp_level > 0 else 0
        self.exp_percent = max(0, min(100, exp_percent))

        segments = 10
        total_gap = gap * (segments - 1)
        seg_width = max(4, (width - total_gap) // segments)

        self._bars = []
        for i in range(segments):
            bar = ctk.CTkProgressBar(
                self,
                width=seg_width,
                height=height,
                corner_radius=corner_radius,
                mode="determinate",
                fg_color=empty_color,
                progress_color=empty_color
            )
            bar.grid(row=0, column=i, padx=(0 if i == 0 else gap), pady=0)
            bar.set(0.0)
            self._bars.append(bar)

        self.set_exp(self.exp_percent)

    def set_exp(self, exp_value):
        segments = len(self._bars)
        v = max(0, min(100, int(exp_value)))
        self.exp_percent = v

        full_segments = int(v // (100 / segments))
        partial = (v % 10) / 10.0

        for i, bar in enumerate(self._bars):
            if i < full_segments:
                bar.set(1.0)
                bar.configure(progress_color="#22c55e")
            elif i == full_segments and full_segments < segments:
                bar.set(partial)
                bar.configure(progress_color="#22c55e")
            else:
                bar.set(0.0)
                bar.configure(progress_color="#171717")


# ----------------- MAIN APP ----------------- #
class TaskManagerApp:
    def __init__(self):
        # --- Theme ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Window ---
        self.root = ctk.CTk()
        self.root.title("Earth Online")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.65)
        window_height = int(screen_height * 0.70)
        self.root.geometry(f"{window_width}x{window_height}")

        # Navigation bar (EXP + menu)
        self.nav_frame = ctk.CTkFrame(self.root, height=110, corner_radius=0)

        # Player
        self.player = Player.load()

        # Tabs
        self.home_tab = HomeTab(self)
        self.calendar_tab = CalendarTab(self)
        self.tasks_tab = TasksTab(self)
        self.stats_tab = StatsTab(self)
        self.journal_tab = JournalTab(self)
        self.notes_tab = NotesTab(self)

        self.current_tab = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        IntroScreen(self, on_finish=lambda: self.show_tab("home"))


    # ----------------- NAV BAR ----------------- #
    def create_navigation(self):
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        player = self.get_player()

        user_name = player.name
        current_xp = player.exp
        xp_level = player.exp_to_next
        level_value = player.level

        self.nav_frame.configure(height=110)
        self.nav_frame.pack(fill="x", padx=0, pady=0)

        exp_wrapper = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        exp_wrapper.pack(side="left", padx=10, pady=5)

        level_square_size = 46
        bar_total_width = int(3.5 * level_square_size)
        bar_height = int(0.52 * level_square_size)

        container_width = level_square_size + 15 + bar_total_width + 40
        container_height = 80

        exp_container = ctk.CTkFrame(
            exp_wrapper,
            width=container_width,
            height=container_height,
            corner_radius=20,
            fg_color="#020617",
            border_color="#4b5563",
            border_width=2
        )
        exp_container.pack()
        exp_container.pack_propagate(False)

        CENTER_Y = container_height // 2
        BAR_LEFT_X = 20 + level_square_size - 4

        exp_bar = SegmentedExpBar(
            exp_container,
            exp_value=current_xp,
            exp_level=xp_level,
            width=bar_total_width,
            height=bar_height
        )
        exp_bar.place(x=BAR_LEFT_X, y=CENTER_Y + 8, anchor="w")

        ctk.CTkLabel(
            exp_container,
            text=f"{user_name}    EXP: {exp_bar.exp_percent}%",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#e5e7eb"
        ).place(
            x=BAR_LEFT_X + bar_total_width / 2,
            y=CENTER_Y - 14,
            anchor="center"
        )

        square = ctk.CTkFrame(
            exp_container,
            width=level_square_size,
            height=level_square_size + 2,
            corner_radius=10,
            fg_color="#0f2218",
            border_color="#38bdf8",
            border_width=2
        )
        square.place(x=20, y=CENTER_Y - level_square_size // 2)

        ctk.CTkLabel(
            square,
            text=str(level_value),
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#e5e7eb"
        ).place(relx=0.5, rely=0.5, anchor="center")

        nav_buttons_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        nav_buttons_frame.pack(side="left", padx=40, pady=18)

        def make_btn(text, tab):
            return ctk.CTkButton(
                nav_buttons_frame,
                text=text,
                width=120,
                height=40,
                corner_radius=12,
                command=lambda: self.show_tab(tab)
            )

        make_btn("Home", "home").pack(side="left", padx=6)
        make_btn("Tasks", "tasks").pack(side="left", padx=6)
        make_btn("Stats", "stats").pack(side="left", padx=6)
        make_btn("Journal", "journal").pack(side="left", padx=6)
        make_btn("Calendar", "calendar").pack(side="left", padx=6)
        make_btn("Notes", "note").pack(side="left", padx=6)

    # ----------------- TAB CONTROL ----------------- #
    def show_tab(self, tab_name):
        if self.current_tab:
            self.current_tab.hide()

        if tab_name == "home":
            self.nav_frame.pack_forget()
        else:
            self.create_navigation()

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
        elif tab_name == "note":
            self.current_tab = self.notes_tab

        self.current_tab.show()

    def get_manager(self):
        return self.tasks_tab.manager

    def get_player(self):
        return self.stats_tab.player

    def refresh_all(self):
        self.tasks_tab.refresh()
        self.stats_tab.refresh()

    def on_close(self):
        self.notes_tab.save_notes()
        self.journal_tab.save_jounral()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TaskManagerApp()
    app.run()