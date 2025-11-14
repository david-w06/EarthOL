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
        self.filename = filename if filename else f"{self.name}_player.json"

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

    def load(self):
        """Load player data if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.level = data.get("level", 1)
                self.exp = data.get("exp", 0)
                self.ovr_exp = data.get("ovr_exp", 0)
                self.exp_to_next = data.get("exp_to_next", int(100 + 0.21 * (self.level) ** 2.38))

                attributes = data.get("attributes", {})
                self.intelligence = attributes.get("intelligence", 0)
                self.knowledge = attributes.get("knowledge", 0)
                self.SE = attributes.get("SE", 0)
                self.athleticism = attributes.get("athleticism", 0)
                self.combat = attributes.get("combat", 0)
                self.artistry = attributes.get("artistry", 0)
                self.looks = attributes.get("looks", 0)
                self.discipline = attributes.get("discipline", 0)