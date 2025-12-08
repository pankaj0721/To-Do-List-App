import json
import os
from copy import deepcopy
from datetime import datetime

TASKS_FILE = 'tasks.json'

class ToDoApp:
    def __init__(self):
        self.tasks = {'todo': [], 'done': []}
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = {'todo': [], 'done': []}

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4)

    def show_tasks(self):
        """Display todo and done tasks"""
        print("\n--- Todo Tasks ---")
        if self.tasks['todo']:
            for i, t in enumerate(self.tasks['todo'], 1):
                print(f"{i}. {t['task']} (Date: {t['date']})")
        else:
            print("No todo tasks.")
        print("\n--- Done Tasks ---")
        if self.tasks['done']:
            for i, t in enumerate(self.tasks['done'], 1):
                print(f"{i}. {t['task']} (Date: {t['date']})")
        else:
            print("No done tasks.")

    def add_task(self):
        task = input("Enter new task: ").strip()
        if not task:
            print("Empty task cannot be added.")
            return

        date_str = input("Enter task date (YYYY-MM-DD) [leave empty for today]: ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")  # validate format
            except ValueError:
                print("Invalid date format. Using today.")
                date_str = datetime.now().strftime("%Y-%m-%d")

        self.tasks['todo'].append({'task': task, 'date': date_str})
        print(f"Task '{task}' added for {date_str}.")
        self.save_tasks()

    def edit_task(self):
        self.show_tasks()
        if not self.tasks['todo']:
            return
        try:
            index = int(input("Enter the number of the task to edit: "))
            new_task = input("Enter the new task text: ").strip()
            if new_task:
                old_task = self.tasks['todo'][index - 1]
                self.tasks['todo'][index - 1] = new_task
                print(f"Task '{old_task}' updated to '{new_task}'.")
                self.save_tasks()
            else:
                print("Empty task cannot be saved.")
        except (ValueError, IndexError):
            print("Invalid input.")

    def mark_done(self):
        self.show_tasks()
        if not self.tasks['todo']:
            return
        try:
            index = int(input("Enter the number of the task to mark done: "))
            task = self.tasks['todo'].pop(index - 1)
            self.tasks['done'].append(task)
            print(f"Task '{task}' marked as done.")
            self.save_tasks()
        except (ValueError, IndexError):
            print("Invalid input.")

    def move_back(self):
        """Move task from done to todo"""
        self.show_tasks()
        if not self.tasks['done']:
            print("No done tasks to move back.")
            return
        try:
            index = int(input("Enter the number of the task to move back: "))
            task = self.tasks['done'].pop(index - 1)
            self.tasks['todo'].append(task)
            print(f"Task '{task}' moved back to todo.")
            self.save_tasks()
        except (ValueError, IndexError):
            print("Invalid input.")

    def delete_task(self):
        self.show_tasks()
        if not self.tasks['todo']:
            return
        try:
            index = int(input("Enter the number of the task to delete: "))
            task = self.tasks['todo'].pop(index - 1)
            print(f"Task '{task}' deleted.")
            self.save_tasks()
        except (ValueError, IndexError):
            print("Invalid input.")

    def clear_done(self):
        if self.tasks['done']:
            self.tasks['done'] = []
            print("All done tasks cleared.")
            self.save_tasks()
        else:
            print("No done tasks to clear.")

    def run(self):
        while True:
            print("\n=== To-Do App Menu ===")
            print("1. Show tasks")
            print("2. Add task")
            print("3. Edit task")
            print("4. Mark task done")
            print("5. Move task back to todo")
            print("6. Delete task")
            print("7. Clear all done tasks")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.show_tasks()
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.edit_task()
            elif choice == '4':
                self.mark_done()
            elif choice == '5':
                self.move_back()
            elif choice == '6':
                self.delete_task()
            elif choice == '7':
                self.clear_done()
            elif choice == '8':
                print("Goodbye! Tasks saved.")
                self.save_tasks()
                break
            else:
                print("Invalid choice. Try again.")


if __name__ == "__main__":
    app = ToDoApp()
    app.run()
