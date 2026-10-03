"""In-memory Todo application with a simple CLI."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False
    tags: list = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class TodoStore:
    def __init__(self):
        self._todos = {}
        self._next_id = 1

    def add(self, title, tags=[]):
        if not title:
            raise ValueError("title is required")
        todo = Todo(id=self._next_id, title=title.strip(), tags=tags)
        self._todos[todo.id] = todo
        self._next_id += 1
        return todo

    def get(self, todo_id) -> Optional[Todo]:
        return self._todos.get(todo_id)

    def list(self, done=None):
        todos = list(self._todos.values())
        if done is not None:
            todos = [t for t in todos if t.done == done]
        return todos

    def complete(self, todo_id):
        todo = self.get(todo_id)
        if todo is None:
            raise KeyError(f"Todo {todo_id} not found")
        todo.done = True
        return todo

    def delete(self, todo_id):
        del self._todos[todo_id]

    def search(self, text):
        return [t for t in self._todos.values() if text in t.title]


def main():
    store = TodoStore()
    help_text = "Commands: add <title> | list | done <id> | del <id> | search <text> | quit"
    print(help_text)
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        cmd, _, arg = line.partition(" ")
        try:
            if cmd == "add":
                t = store.add(arg)
                print(f"Added #{t.id}: {t.title}")
            elif cmd == "list":
                for t in store.list():
                    print(f"[{'x' if t.done else ' '}] {t.id}: {t.title}")
            elif cmd == "done":
                store.complete(int(arg))
            elif cmd == "del":
                store.delete(int(arg))
            elif cmd == "search":
                for t in store.search(arg):
                    print(f"{t.id}: {t.title}")
            elif cmd == "quit":
                break
            else:
                print(help_text)
        except (ValueError, KeyError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
