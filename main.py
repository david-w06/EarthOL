import customtkinter as ctk


class HomeTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root

        # Declare attributes here (with types if you want)
        self.home_frame: ctk.CTkFrame | None = None
        self.title_label: ctk.CTkLabel | None = None
        self.welcome_label: ctk.CTkLabel | None = None

        # Animation variables (fine here)
        self.alpha = 0.0
        self.fade_in = True
        self.current_text_index = 0
        self.texts = [
            "People love video games, The thrill of leveling up",
            "Unlocking new skills, Watching numbers rise",
            "But in chasing virtual progress",
            "How many of us forget the greatest game of all",
            "Running for 4.57 billion years",
            "Across 197 servers",
            "With over 8 billion active players",
            "And a map spanning 510 million square kilometers",
            "No respawns, No cheating, One account for lifetime",
            "Welcome to Earth Online",
            "This application is your interface to life itself",
            "A productivity tracker and task visualizer designed",
            "to help you level up in the only game that truly matters",
            "Let's get started"
        ]

        self.create_ui()

    def create_ui(self):
        """Create all UI elements for home tab"""
        # Main frame
        self.home_frame = ctk.CTkFrame(self.root, corner_radius=20)

        # Title
        self.title_label = ctk.CTkLabel(
            self.home_frame,
            text="EARTH ONLINE",
            font=ctk.CTkFont("Trebuchet MS", size=68),
            text_color="#ffffff",
        )
        self.title_label.pack(pady=(40, 8))

        # Animated welcome text
        self.welcome_label = ctk.CTkLabel(
            self.home_frame,
            text=self.texts[self.current_text_index],
            font=ctk.CTkFont(size=18),
            text_color="white",
            wraplength=780,
            justify="center",
        )
        self.welcome_label.pack(pady=(8, 28))

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
                height=60,
                corner_radius=18,
                font=ctk.CTkFont(size=20, weight="bold"),
                command=lambda: self.main_app.show_tab(tab_name),
            )

        big_button("📋 Today's Tasks", "tasks").pack(pady=12)
        big_button("📊 Player Stats", "stats").pack(pady=12)
        big_button("📓 Journal", "tasks").pack(pady=12)  # Placeholder - goes to tasks for now
        big_button("📅 Calendar", "tasks").pack(pady=12)  # Placeholder - goes to tasks for now

    def show(self):
        """Display the home tab and start animations"""
        self.home_frame.pack(fill="both", expand=True, padx=24, pady=24)
        self.start_fade_animation()

    def hide(self):
        """Hide the home tab"""
        self.home_frame.pack_forget()

    def start_fade_animation(self):
        """Start the text fade animation"""
        self.alpha = 0
        self.fade_in = True
        self.current_text_index = 0
        self.welcome_label.configure(text=self.texts[self.current_text_index])
        self.update_fade()

    def update_fade(self):
        """Update fade animation"""
        if self.current_text_index >= len(self.texts) - 1 and self.alpha >= 1:
            self.welcome_label.configure(text_color='#ffffff')
            return

        if self.fade_in:
            self.alpha += 0.05
            if self.alpha >= 1:
                self.alpha = 1
                self.fade_in = False
                self.root.after(1000, self.update_fade)
                return
        else:
            self.alpha -= 0.05
            if self.alpha <= 0:
                self.alpha = 0
                self.fade_in = True
                self.current_text_index += 1

                if self.current_text_index >= len(self.texts):
                    self.alpha = 1
                    return

                self.welcome_label.configure(text=self.texts[self.current_text_index])

        # Convert alpha to grayscale value
        gray_value = int(self.alpha * 255)
        color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
        self.welcome_label.configure(text_color=color)
        self.root.after(50, self.update_fade)
