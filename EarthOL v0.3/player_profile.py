import os
import json


class Player:
    def __init__(self, name, filename=None):
        self.name = name
        self.level = 1
        self.exp = 0
        self.ovr_exp = 0
        self.exp_to_next = int(100 + 0.21 * (self.level) ** 2.38)

        # Attributes
        self.intelligence = 0
        self.knowledge = 0
        self.SE = 0
        self.athleticism = 0
        self.combat = 0
        self.artistry = 0
        self.looks = 0
        self.discipline = 0

        # Save file name
        self.filename = filename if filename else "player.json"

    def add_experience(self, amount):
        """Add experience and handle leveling up."""
        self.exp += amount
        self.ovr_exp += amount
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level_up()

    def level_up(self):
        """Increase level and adjust required experience."""
        self.level += 1
        self.exp_to_next = int(100 + 0.21 * (self.level) ** 2.38)
        print(f"🎉 Level up! You are now level {self.level}.")

    def save(self):
        """Save player data to file."""
        data = {
            "level": self.level,
            "exp": self.exp,
            "ovr_exp": self.ovr_exp,
            "exp_to_next": self.exp_to_next,
            "attributes": {
                "intelligence": self.intelligence,
                "knowledge": self.knowledge,
                "SE": self.SE,
                "athleticism": self.athleticism,
                "combat": self.combat,
                "artistry": self.artistry,
                "looks": self.looks,
                "discipline": self.discipline
            }
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filename="player.json"):
        if not os.path.exists(filename):
            return cls("Unknown")

        try:
            with open(filename, "r") as f:
                data = json.load(f)

            player = cls(data.get("name", "Unknown"))

            player.level = data.get("level", 1)
            player.exp = data.get("exp", 0)
            player.ovr_exp = data.get("ovr_exp", 0)
            player.exp_to_next = data.get(
                "exp_to_next",
                int(100 + 0.21 * player.level ** 2.38)
            )

            attrs = data.get("attributes", {})
            player.intelligence = attrs.get("intelligence", 0)
            player.knowledge = attrs.get("knowledge", 0)
            player.SE = attrs.get("SE", 0)
            player.athleticism = attrs.get("athleticism", 0)
            player.combat = attrs.get("combat", 0)
            player.artistry = attrs.get("artistry", 0)
            player.looks = attrs.get("looks", 0)
            player.discipline = attrs.get("discipline", 0)

            return player

        except json.JSONDecodeError:
            print("Save file corrupted.")
            return cls("Unknown")

