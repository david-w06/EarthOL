import customtkinter as ctk
import tkinter as tk
import warnings
import theme

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
        self.home_frame = ctk.CTkFrame(self.root, corner_radius=20, fg_color="transparent")
        warnings.filterwarnings("ignore", message=".*Given image is not CTkImage.*")

        full_res_photo = tk.PhotoImage(file="eol logo 2.png")
        self.logo_photo = full_res_photo.subsample(4, 4)

        # Header Container
        header_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        header_frame.pack(pady=(40, 20), padx=20)

        self.header_label = ctk.CTkLabel(
            header_frame,
            text=" EARTH ONLINE",  # Added a space at the start for padding
            image=self.logo_photo,
            compound="left",
            font=ctk.CTkFont("Trebuchet MS", size=48, weight="bold"), # Slightly larger
            text_color=theme.TEXT_PRIMARY,
        )
        self.header_label.pack()

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
                width=340,
                height=60,
                corner_radius=18,
                font=ctk.CTkFont("Segoe UI", size=22, weight="bold"),
                fg_color=theme.BTN_BG,
                hover_color=theme.BTN_HOVER,
                border_width=1,
                border_color=theme.BORDER_NORMAL,
                text_color=theme.TEXT_PRIMARY,
                command=lambda: self.main_app.show_tab(tab_name),
            )

        # Added consistent spacing
        big_button("📋 Today's Tasks", "tasks").pack(pady=10)
        big_button("📊 Player Stats", "stats").pack(pady=10)
        big_button("📓 Journal", "journal").pack(pady=10)
        big_button("📅 Calendar", "calendar").pack(pady=10)
        big_button("📝 Note", "note").pack(pady=10)

    def show(self):
        """Display the home tab """
        self.home_frame.pack(fill="both", expand=True, padx=24, pady=24)

    def hide(self):
        """Hide the home tab"""
        self.home_frame.pack_forget()

