import customtkinter as ctk

class CalenderTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root

        self.create_ui()

    def create_ui(self):
        """Create all UI elements for stats tab"""
        # Main frame
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16)

    def show(self):
        """Display the stats tab"""
        self.stats_frame.pack(pady=10, padx=16, fill="both", expand=True)
        self.refresh()

    def hide(self):
        """Hide the stats tab"""
        self.stats_frame.pack_forget()

    def refresh(self):
        """Refresh the stats display with current player data"""
        # Clear existing widgets
        for widget in self.stats_frame.winfo_children():
            widget.destroy()