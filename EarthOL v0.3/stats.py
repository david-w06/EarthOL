import customtkinter as ctk
from player_profile import Player


class StatsTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root
        self.player = main_app.player
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

        # Title
        title_label = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Player Statistics",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))

        # Stats container
        stats_container = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        stats_container.pack(fill="both", expand=True, padx=20)

        label_font_bold = ctk.CTkFont(size=12, weight="bold")
        r = 0

        # Player level and experience
        ctk.CTkLabel(stats_container, text="Level:", font=label_font_bold).grid(row=r, column=0, sticky="w", padx=6,
                                                                                pady=8)
        ctk.CTkLabel(stats_container, text=str(self.player.level), font=ctk.CTkFont(size=14)).grid(row=r, column=1,
                                                                                                   sticky="w", padx=6,
                                                                                                   pady=8)
        r += 1

        ctk.CTkLabel(stats_container, text="Experience:", font=label_font_bold).grid(row=r, column=0, sticky="w",
                                                                                     padx=6, pady=8)
        ctk.CTkLabel(stats_container, text=f"{int(self.player.exp)}/{self.player.exp_to_next}",
                     font=ctk.CTkFont(size=14)).grid(row=r, column=1, sticky="w", padx=6, pady=8)
        r += 1

        ctk.CTkLabel(stats_container, text="Total XP:", font=label_font_bold).grid(row=r, column=0, sticky="w", padx=6,
                                                                                   pady=8)
        ctk.CTkLabel(stats_container, text=f"{self.player.ovr_exp:.1f}", font=ctk.CTkFont(size=14)).grid(row=r,
                                                                                                         column=1,
                                                                                                         sticky="w",
                                                                                                         padx=6, pady=8)
        r += 1

        # Separator
        separator = ctk.CTkFrame(stats_container, height=2, fg_color="gray")
        separator.grid(row=r, column=0, columnspan=2, sticky="ew", padx=10, pady=15)
        r += 1

        # Attributes header
        ctk.CTkLabel(stats_container, text="Attributes", font=ctk.CTkFont(size=16, weight="bold")).grid(row=r, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=10)
        r += 1

        # Attributes
        stats = {
            "🧠 Intelligence": self.player.intelligence,
            "📚 Knowledge": self.player.knowledge,
            "💝 Social & Emotional": self.player.SE,
            "💪 Athleticism": self.player.athleticism,
            "⚔️ Combat": self.player.combat,
            "🎨 Artistry": self.player.artistry,
            "✨ Looks": self.player.looks,
            "📏 Discipline": getattr(self.player, 'discipline', 0)
        }

        for stat_name, value in stats.items():
            ctk.CTkLabel(stats_container, text=stat_name, font=label_font_bold).grid(row=r, column=0, sticky="w",
                                                                                     padx=6, pady=6)
            ctk.CTkLabel(stats_container, text=f"{value:.1f}", font=ctk.CTkFont(size=12)).grid(row=r, column=1,
                                                                                               sticky="w", padx=6,
                                                                                               pady=6)
            r += 1