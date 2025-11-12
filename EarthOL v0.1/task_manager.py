import json


class Task:
    VALID_CATEGORIES = [
        "School Work", "Self-Study-STEM", "Self-Study-Humanities", "Workout",
        "Combat Training", "Looks", "Practice Music", "Practice Arts",
        "Play Sports", "Others"
    ]

    def __init__(self, name, scheduled_time, category, duration, note="", completed=False, exp=0):
        self.name = name
        self.scheduled_time = scheduled_time
        self.category = category
        self.duration = duration
        self.note = note
        self.completed = completed
        self.exp = exp

    def mark_done(self):
        self.completed = not self.completed

    def to_dict(self):
        return {
            "name": self.name,
            "scheduled_time": self.scheduled_time,
            "category": self.category,
            "duration": self.duration,
            "note": self.note,
            "completed": self.completed,
            "exp": self.exp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            scheduled_time=data.get("scheduled_time", "No time"),
            category=data.get("category", "General"),
            duration=int(data.get("duration", 0)),
            note=data.get("note", ""),
            completed=data.get("completed", False),
            exp=data.get("exp", 0)
        )

    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.name} | {self.category} | {self.scheduled_time} | {self.duration} min | {self.note}"


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

    def add_task(self, name, scheduled_time="No time", category="General", duration=0, note="", completed=False, exp=0):
        new_task = Task(name, scheduled_time, category, duration, note, completed, exp)
        self.tasks.append(new_task)
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