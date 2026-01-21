import customtkinter as ctk
import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox
from entry import JournalEntry
import json
import os

# ------------Global journal state variable----------------------
STATE_FILE = "journal_state.json"

def load_journal_state():
    today = date.today().isoformat()
    default_state = {"journaled": False, "last_date": today}
    if not os.path.exists(STATE_FILE):
        return default_state

    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

        # RESET LOGIC: If the saved date isn't today, reset to False
        if state.get("last_date") != today:
            state = default_state
            save_journal_state(state)
        return state
    except:
        return default_state


def save_journal_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

# --- GLOBAL INITIALIZATION ---
_state = load_journal_state()
Journal = _state["journaled"]
_last_reset = date.today()

def mark_as_journaled():
    """Call this when a user successfully saves a journal entry"""
    global Journal
    Journal = True
    save_journal_state({"journaled": True, "last_date": date.today().isoformat()})

class JournalTab:
    def __init__(self, main_app):
        self.main_app = main_app
        self.root = main_app.root

        # Create frame and UI, but do NOT pack it
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16)
        self.create_ui()

    def create_ui(self):
        """Create all UI elements for journal tab"""
        self.stats_frame = ctk.CTkFrame(self.root, corner_radius=16)

        title_label = ctk.CTkLabel(
            self.stats_frame,
            text="📋 Journal",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 5))

        # Button frame
        button_frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="➕ Add Entry", command=self.open_add_entry_window).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="📓 Read", command=self.open_entry).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑️ Delete", command=self.delete_entry).pack(side="left", padx=5)

        # Listbox Frame
        listbox_frame = ctk.CTkFrame(self.stats_frame)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(listbox_frame, text="Your Journal Entries:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(5, 0))

        self.task_listbox = tk.Listbox(
            listbox_frame,
            width=90,
            height=18,
            bg="#111111",
            fg="white",
            selectforeground="white",
            highlightbackground="#111111",
            borderwidth=0,
            selectbackground="#2a85ff",
            font=("Arial", 14)
        )
        self.task_listbox.pack(fill="both", expand=True, padx=6, pady=6)

    # -----------------------------
    # Add Entry Window
    # -----------------------------
    def open_add_entry_window(self):
        add_window = ctk.CTkToplevel(self.root)
        add_window.title("New Entry")
        add_window.geometry("300x200")
        add_window.grab_set()

        wrap = ctk.CTkFrame(add_window, corner_radius=12)
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(wrap, text="Choose a Date:").pack(anchor="w", pady=(6, 2))
        date_entry = ctk.CTkEntry(wrap, width=300, placeholder_text="YYYY-MM-DD")
        date_entry.pack(pady=4)

        def open_entry_textbox():
            input_str = date_entry.get().strip()
            try:
                input_date = datetime.strptime(input_str, "%Y-%m-%d").date().isoformat()
            except ValueError:
                messagebox.showwarning("Warning", "Date format incorrect. Use YYYY-MM-DD.")
                return

            # 1. Close the date-picker window FIRST
            add_window.destroy()

            # 2. Open the entry window AFTER a tiny delay (100ms)
            # This ensures the old window is completely gone from the focus stack
            entry = JournalEntry(input_date, "")
            self.root.after(100, lambda: entry.open_textbox(self.root, refresh_callback=self.refresh_listbox))
            mark_as_journaled()

        ctk.CTkButton(wrap, text="Done", command=open_entry_textbox).pack(pady=12)

    # -----------------------------
    # Helpers
    # -----------------------------
    def show(self):
        self._check_reset() #check for journal refresh
        self.stats_frame.pack(pady=10, padx=16, fill="both", expand=True)
        self.refresh_listbox()

    def hide(self):
        self.stats_frame.pack_forget()

    def refresh_listbox(self):
        """Reload the list of journal entries into the listbox"""
        self.task_listbox.delete(0, "end")
        entries = JournalEntry.load()
        for e in entries:
            self.task_listbox.insert("end", e.input_date)

    def _check_reset(self):
        """Check if date changed while app was running"""
        global Journal, _last_reset
        today = date.today()
        if today != _last_reset:
            Journal = False
            _last_reset = today
            save_journal_state({"journaled": False, "last_date": today.isoformat()})

    # Placeholder methods for completeness
    def open_entry(self):
        selected = self.task_listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        entries = JournalEntry.load()
        entry = entries[idx]
        entry.open_textbox(self.root, refresh_callback=self.refresh_listbox)

    def delete_entry(self):
        # 1. Get the selected index from the Listbox
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Delete", "Please select an entry to delete.")
            return

        # 2. Get the date string of the selected entry
        # We use the text in the listbox to find the right entry in the file
        date_to_delete = self.task_listbox.get(selected[0])

        # 3. Confirmation Dialog
        confirm = messagebox.askyesno("Confirm", f"Delete the entry for {date_to_delete}?")
        if not confirm:
            return

        # 4. Load all current entries from the file
        entries = JournalEntry.load()

        # 5. Filter the list to remove the matching date
        # This creates a new list excluding the one the user selected
        updated_entries = [e for e in entries if e.input_date != date_to_delete]

        # 6. Save the updated list back to the JSON file
        # We convert the objects back to dictionaries for JSON storage
        import json
        data = [e.to_dict() for e in updated_entries]
        with open("journal.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        # 7. Refresh the UI so the entry disappears immediately
        self.refresh_listbox()
        messagebox.showinfo("Deleted", "Entry removed successfully.")

    def save_jounral(self):
        return






