import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from home import HomeTab
from ttask import TasksTab
from stats import StatsTab
from journal import JournalTab
from calendar_tab import CalendarTab


# ----------------- EXP SYSTEM ----------------- #
class SegmentedExpBar(ctk.CTkFrame):
    def __init__(self, master, exp_value, exp_level, width=340, height=24,
                 gap=1, corner_radius=3, empty_color="#171717"):
        super().__init__(master, fg_color="transparent")

        exp_percent = round((exp_value / exp_level) * 100) if exp_level > 0 else 0
        self.exp_percent = max(0, min(100, exp_percent))  # clamp 0–100

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
        v = max(0, min(100, int(exp_value)))  # value out of 100
        self.exp_percent = v                  # keep in sync

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

        # proportional screen for the user instead of a locked small screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.65)
        window_height = int(screen_height * 0.65)
        self.root.geometry(f"{window_width}x{window_height}")
        # self.root.resizable(False, False) #lock window size

        # Create navigation frame (top bar)
        self.nav_frame = ctk.CTkFrame(self.root, height=110, corner_radius=0)

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

        # Get live Player data from stats tab
        player = self.get_player()
        user_name = player.name
        current_xp = player.exp          # XP toward next level
        xp_level = player.exp_to_next    # XP needed for next level
        level_value = player.level       # Level number for the square

        # Make sure nav frame is visible and full width
        self.nav_frame.configure(height=110)
        self.nav_frame.pack(fill="x", padx=0, pady=0)
        exp_wrapper = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        exp_wrapper.pack(side="left", padx=10, pady=5)

        # exp system properties 
        level_square_size = 46              
        bar_total_width = int(3.5 * level_square_size)  
        bar_height = int(0.52 * level_square_size)
        CONTAINER_PADDING_Y = 13          
        CONTAINER_PADDING_X = 20         

        # container width/height
        container_width = (
            level_square_size + 15
            + bar_total_width
            + 2 * CONTAINER_PADDING_X 
        )
        content_height = 54          
        container_height = content_height + 2 * CONTAINER_PADDING_Y 

        # Outer container box for the whole EXP system
        exp_container = ctk.CTkFrame(
            exp_wrapper,
            width=container_width,
            height=container_height,
            corner_radius=20,
            fg_color="#020617",     
            border_color="#4b5563",
            border_width=2
        )
        exp_container.pack(side="left")
        exp_container.pack_propagate(False)


        board = exp_container
        CENTER_Y = container_height // 2
        BAR_LEFT_X = 20 + level_square_size - 4
        exp_label_top = CENTER_Y + 5 - bar_height / 2 - 6 - 19

        # square slightly taller than wide
        square_height = level_square_size + 2
        square_y = CENTER_Y - square_height // 2


        # --- EXP bar (10 segments, all visible) ---
        exp_bar = SegmentedExpBar(
            board,
            exp_value=current_xp,
            exp_level=xp_level,
            width=bar_total_width,
            height=bar_height,
            gap=1,
            corner_radius=max(1, bar_height // 8),
        )
        exp_bar.place(
            x=BAR_LEFT_X,
            y=CENTER_Y + 5,
            anchor="w"
        )


        # --- EXP label above the bar ---
        exp_label = ctk.CTkLabel(
            board,
            text=f"{user_name}    EXP: {exp_bar.exp_percent}%",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#e5e7eb",
            fg_color="transparent"
        )
        exp_label.place(
            x=BAR_LEFT_X + bar_total_width / 2,
            y=exp_label_top + 19 / 2,
            anchor="center"
        )


        # --- Level square box ---
        square = ctk.CTkFrame(
            board,
            width=level_square_size,
            height=square_height,
            corner_radius=max(8, level_square_size // 5),
            fg_color="#0f2218",
            border_color="#38bdf8",  
            border_width=2
        )
        square.place(x=20, y=square_y)
        square.lift()  # keep on top

        # in square is the player.level
        level_number = ctk.CTkLabel(
            square,
            text=str(level_value),
            font=ctk.CTkFont(size=max(24, level_square_size // 2 + 6), weight="bold"),
            text_color="#e5e7eb",
            fg_color="transparent"
        )
        level_number.place(relx=0.5, rely=0.5, anchor="center")



        # ------------- RIGHT: NAVIGATION BUTTONS  ------------- #
        nav_buttons_frame = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        nav_buttons_frame.pack(side="left", padx=40, pady=18)

        button_height = 40     # you said nav bar is good now, so leave this
        button_width = 100

        def make_btn(text, tab):
            return ctk.CTkButton(
                nav_buttons_frame,
                text=text,
                width=button_width,
                height=button_height,
                corner_radius=12,
                command=lambda: self.show_tab(tab)
            )

        make_btn("Home", "home").pack(side="left", padx=6)
        make_btn("Tasks", "tasks").pack(side="left", padx=6)
        make_btn("Stats", "stats").pack(side="left", padx=6)
        make_btn("Journal", "journal").pack(side="left", padx=6)
        make_btn("Calendar", "calendar").pack(side="left", padx=6)

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
