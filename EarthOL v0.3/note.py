import customtkinter as ctk

class NotesTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root
        self.create_ui()
        self.load_notes()

    def create_ui(self):
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16)

        # Title
        title = ctk.CTkLabel(
            self.stats_frame,
            text="Notes",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(10, 5))

        # Text area (THIS is the note interface)
        self.textbox = ctk.CTkTextbox(
            self.stats_frame,
            wrap="word"
        )
        self.textbox.pack(
            padx=10,
            pady=10,
            fill="both",
            expand=True
        )

    def show(self):
        """Display the stats tab"""
        self.stats_frame.pack(pady=10, padx=16, fill="both", expand=True)

    def hide(self):
        self.stats_frame.pack_forget()

    def save_notes(self):
        text = self.textbox.get("1.0", "end-1c")
        with open("notes.txt", "w", encoding="utf-8") as f:
            f.write(text)

    def load_notes(self):
        try:
            with open("notes.txt", "r", encoding="utf-8") as f:
                self.textbox.insert("1.0", f.read())
        except FileNotFoundError:
            pass
