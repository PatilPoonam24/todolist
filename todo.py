"""
Simple CLI To-Do app for Windows.

Usage examples (from Command Prompt / PowerShell):
    python todo.py add "Buy milk"
    python todo.py list
    python todo.py done 1
    python todo.py remove 2
"""

import sys
import json
from pathlib import Path

DATA_FILE = Path("data.json")

def load_data():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text())

def save_data(todos):
    DATA_FILE.write_text(json.dumps(todos, indent=2))

def list_todos(todos):
    if not todos:
        print("No tasks. Add one with: python todo.py add \"Task description\"")
        return
    for i, item in enumerate(todos, start=1):
        status = "✔" if item.get("done") else " "
        print(f"{i}. [{status}] {item['text']}")

def add_todo(todos, text):
    todos.append({"text": text, "done": False})
    save_data(todos)
    print("Added:", text)

def mark_done(todos, index):
    try:
        todos[index - 1]["done"] = True
        save_data(todos)
        print("Marked done:", todos[index - 1]["text"])
    except IndexError:
        print("Invalid task number.")

def remove_todo(todos, index):
    try:
        removed = todos.pop(index - 1)
        save_data(todos)
        print("Removed:", removed["text"])
    except IndexError:
        print("Invalid task number.")

def show_help():
    print(__doc__)

def main():
    todos = load_data()
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()
    if cmd == "list":
        list_todos(todos)
    elif cmd == "add" and len(sys.argv) >= 3:
        add_todo(todos, " ".join(sys.argv[2:]))
    elif cmd == "done" and len(sys.argv) == 3 and sys.argv[2].isdigit():
        mark_done(todos, int(sys.argv[2]))
    elif cmd == "remove" and len(sys.argv) == 3 and sys.argv[2].isdigit():
        remove_todo(todos, int(sys.argv[2]))
    else:
        show_help()

if __name__ == "__main__":
    main()
