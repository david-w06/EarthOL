import customtkinter as ctk
import tkinter as tk
import warnings

class HomeTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root

        # Declare attributes here (with types if you want)
        self.home_frame: ctk.CTkFrame | None = None
        self.title_label: ctk.CTkLabel | None = None
        self.welcome_label: ctk.CTkLabel | None = None

        self.create_ui()

    def create_ui(self):
        """Create all UI elements for home tab"""
        # Main frame
        self.home_frame = ctk.CTkFrame(self.root, corner_radius=20)
        warnings.filterwarnings("ignore", message=".*Given image is not CTkImage.*")

        full_res_photo = tk.PhotoImage(file="eol logo 2.png")
        self.logo_photo = full_res_photo.subsample(4, 4)

        self.header_label = ctk.CTkLabel(
            self.home_frame,
            text=" EARTH ONLINE",  # Added a space at the start for padding
            image=self.logo_photo,
            compound="left",
            font=ctk.CTkFont("Trebuchet MS", size=40, weight="bold"),
            text_color="#ffffff",
        )
        self.header_label.pack(pady=(40, 8), padx=20)

        # Navigation buttons
        btn_wrap = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        btn_wrap.pack(expand=True)

        self.create_navigation_buttons(btn_wrap)

    def create_navigation_buttons(self, parent):
        """Create navigation buttons"""

        def big_button(text, tab_name):
            return ctk.CTkButton(
                parent,
                text=text,
                width=320,
                height=50,
                corner_radius=18,
                font=ctk.CTkFont(size=20, weight="bold"),
                command=lambda: self.main_app.show_tab(tab_name),
            )

        big_button("📋 Today's Tasks", "tasks").pack(pady=12)
        big_button("📊 Player Stats", "stats").pack(pady=12)
        big_button("📓 Journal", "journal").pack(pady=12)
        big_button("📅 Calendar", "calender").pack(pady=12)
        big_button("📝 Note", "note").pack(pady=12)

    def show(self):
        """Display the home tab """
        self.home_frame.pack(fill="both", expand=True, padx=24, pady=24)

    def hide(self):
        """Hide the home tab"""
        self.home_frame.pack_forget()

