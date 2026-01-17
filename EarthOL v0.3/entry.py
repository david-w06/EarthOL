import json
import os
from datetime import date
import customtkinter as ctk


class JournalEntry:
    def __init__(self, input_date: str, text: str = ""):
        self.input_date = input_date
        self.text = text

    def to_dict(self):
        return {
            "input_date": self.input_date,
            "text": self.text
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            input_date=data["input_date"],
            text=data["text"]
        )

    def save(self, filename="journal.json"):
        data = []
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []

        # Logic to update existing date or add new one
        updated = False
        for i, entry in enumerate(data):
            if entry["input_date"] == self.input_date:
                data[i] = self.to_dict()
                updated = True
                break

        if not updated:
            data.append(self.to_dict())

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(filename="journal.json"):
        if not os.path.exists(filename):
            return []
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [JournalEntry.from_dict(d) for d in data]
        except (json.JSONDecodeError, KeyError):
            return []

    # --- FIXED UI FUNCTIONS ---

    def open_textbox(self, root, refresh_callback=None):  # Added 'self'
        """
        Opens a popup window for this specific entry.
        """
        add_window = ctk.CTkToplevel(root)
        add_window.title(f"Journal Entry: {self.input_date}")
        add_window.geometry("600x450")
        add_window.grab_set()

        # Textbox
        textbox = ctk.CTkTextbox(add_window, font=("Arial", 14))
        textbox.pack(expand=True, fill="both", padx=20, pady=20)

        # Load existing text if this object already has some
        if self.text:
            textbox.insert("1.0", self.text)

        def save_and_close():
            # Update the object's text from the textbox
            self.text = textbox.get("1.0", "end-1c")
            self.save()
            if refresh_callback:
                refresh_callback()  # Trigger the refresh in JournalTab

            add_window.destroy()

        save_button = ctk.CTkButton(add_window, text="Save & Close", command=save_and_close)
        save_button.pack(pady=(0, 20))


    def save_textbox(textbox, window):
        """
        Saves the content of a textbox into a JournalEntry and closes the window
        """
        text = textbox.get("1.0", "end-1c")
        entry = JournalEntry(date.today().isoformat(), text)
        entry.save()
        window.destroy()


    def load_textbox(textbox, text):
        """
        Loads given text into a textbox
        """
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)

