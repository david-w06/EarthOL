import customtkinter as ctk

class IntroScreen:
    def __init__(self, main_app, on_finish):
        self.main_app = main_app
        self.root = main_app.root
        self.on_finish = on_finish

        self.frame = ctk.CTkFrame(self.root, fg_color="black")
        self.frame.pack(fill="both", expand=True)

        self.alpha = 0.0
        self.fade_in = True
        self.current_text_index = 0

        # handling skip
        self.finished = False
        self.frame.bind("<Button-1>", self.skip)
        self.root.bind("<Button-1>", self.skip)
        self.root.bind("<Key>", self.skip)

        hint = ctk.CTkLabel(
            self.frame,
            text="Click anywhere to skip",
            text_color="#555555",
            font=ctk.CTkFont(size=12),
        )
        hint.place(relx=0.5, rely=0.95, anchor="center")

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

        self.label = ctk.CTkLabel(
            self.frame,
            text=self.texts[0],
            font=ctk.CTkFont(size=20),
            text_color="black",
            wraplength=780,
            justify="center",
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.update_fade()

    def update_fade(self):
        if self.finished:
            return

        if self.current_text_index >= len(self.texts) - 1 and self.alpha >= 1:
            self.label.configure(text_color="#ffffff")
            self.root.after(800, self.finish)
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

                if self.current_text_index < len(self.texts):
                    self.label.configure(text=self.texts[self.current_text_index])

        gray = int(self.alpha * 255)
        color = f'#{gray:02x}{gray:02x}{gray:02x}'
        self.label.configure(text_color=color)

        self.root.after(50, self.update_fade)

    def finish(self):
        if self.finished:
            return

        self.finished = True

        # Unbind events
        self.root.unbind("<Button-1>")
        self.root.unbind("<Key>")

        # Destroy intro
        self.frame.destroy()

        # Go to home
        self.on_finish()

    def skip(self, event=None):
        self.finish()


