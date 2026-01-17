import json
from datetime import datetime

class Task:
    VALID_CATEGORIES = [
        "School Work", "Self-Study-STEM", "Self-Study-Humanities", "Workout",
        "Combat Training", "Looks", "Practice Music", "Practice Arts",
        "Play Sports", "Others"
    ]

    def __init__(self, name, start_time, category, duration, note="", completed=False, exp=0):
        self.name = name
        self.start_time = start_time  # datetime | None
        self.category = category
        self.duration = duration  # minutes
        self.note = note
        self.completed = completed
        self.exp = exp

    def mark_done(self):
        self.completed = not self.completed

    def to_dict(self):
        return {
            "name": self.name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "category": self.category,
            "duration": self.duration,
            "completed": self.completed,
            "note": self.note
        }

    @classmethod
    def from_dict(cls, data):
        start_time = (
            datetime.fromisoformat(data["start_time"])
            if data["start_time"]
            else None
        )

        return cls(
            name=data["name"],
            start_time=start_time,
            category=data["category"],
            duration=data["duration"],
            completed=data.get("completed", False),
            note=data.get("note", "")
        )

    def __str__(self):
        time_str = (
            self.start_time.strftime("%Y-%m-%d %H:%M")
            if self.start_time
            else "No time"
        )

        status = "✅" if self.completed else "⬜"
        return f"{status} {self.name} | {time_str} | {self.category} | {self.duration} min"


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def get_task(self, name):
        for task in self.tasks:
            if task.name == name:
                return task
        return None

    def add_task(self, name, start_time, category, duration, note):
        task = Task(name, start_time, category, duration, note)
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, name):
        self.tasks = [t for t in self.tasks if t.name != name]
        self.save_tasks()

    def mark_done(self, name):
        for task in self.tasks:
            if task.name == name:
                task.mark_done()
                break
        self.save_tasks()

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)

    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(d) for d in data]
        except FileNotFoundError:
            self.tasks = []