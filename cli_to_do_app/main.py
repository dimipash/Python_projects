import sqlite3
import typer
import datetime
from typing import List, Tuple

app = typer.Typer()


class TaskManager:
    def __init__(self, db_name: str = "todo.db"):
        """
        Initialize the TaskManager and ensure the tasks table exists.
        """
        try:
            self.conn = sqlite3.connect(db_name)
            self.conn.row_factory = sqlite3.Row
            self.create_table()
        except sqlite3.Error as e:
            typer.echo(f"Database connection error: {e}")
            raise

    def create_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                status BOOLEAN NOT NULL DEFAULT 0,
                creation_date TEXT NOT NULL,
                completion_date TEXT
            )
            """
            self.conn.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            typer.echo(f"Error creating table: {e}")
            raise

    def add_task(self, description: str) -> None:
        if not description.strip():
            raise ValueError("Task description cannot be empty.")

        # Check for duplicate tasks (same description and not completed)
        cursor = self.conn.execute(
            "SELECT id FROM tasks WHERE description = ? AND status = 0", (description,)
        )
        if cursor.fetchone():
            raise ValueError("Duplicate task: Task already exists.")

        now = datetime.datetime.now().isoformat()
        try:
            self.conn.execute(
                "INSERT INTO tasks (description, status, creation_date) VALUES (?, 0, ?)",
                (description, now),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            typer.echo(f"Error adding task: {e}")
            raise

    def list_tasks(self) -> List[sqlite3.Row]:
        try:
            cursor = self.conn.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            return tasks
        except sqlite3.Error as e:
            typer.echo(f"Error retrieving tasks: {e}")
            raise

    def complete_task(self, task_id: int) -> None:
        now = datetime.datetime.now().isoformat()
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            raise ValueError("Invalid task ID: Task not found.")

        try:
            self.conn.execute(
                "UPDATE tasks SET status = 1, completion_date = ? WHERE id = ?",
                (now, task_id),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            typer.echo(f"Error marking task complete: {e}")
            raise

    def remove_task(self, task_id: int) -> None:
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()
        if not task:
            raise ValueError("Invalid task ID: Task not found.")

        try:
            self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            typer.echo(f"Error removing task: {e}")
            raise

    def stats(self) -> Tuple[int, int, int]:
        try:
            cursor = self.conn.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]
            cursor = self.conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 1")
            completed = cursor.fetchone()[0]
            pending = total - completed
            return total, completed, pending
        except sqlite3.Error as e:
            typer.echo(f"Error retrieving task statistics: {e}")
            raise


task_manager = TaskManager()


@app.command()
def add(description: str):
    try:
        task_manager.add_task(description)
        typer.echo("Task added successfully.")
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command()
def list():
    try:
        tasks = task_manager.list_tasks()
        if not tasks:
            typer.echo("No tasks found.")
            return
        for task in tasks:
            status = "Completed" if task["status"] else "Pending"
            typer.echo(f'{task["id"]}: {task["description"]} - {status}')
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command()
def complete(task_id: int):
    try:
        task_manager.complete_task(task_id)
        typer.echo("Task marked as complete.")
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command()
def remove(task_id: int):
    try:
        task_manager.remove_task(task_id)
        typer.echo("Task removed successfully.")
    except Exception as e:
        typer.echo(f"Error: {e}")


@app.command()
def stats():
    try:
        total, completed, pending = task_manager.stats()
        typer.echo(f"Total tasks: {total}")
        typer.echo(f"Completed tasks: {completed}")
        typer.echo(f"Pending tasks: {pending}")
    except Exception as e:
        typer.echo(f"Error: {e}")


if __name__ == "__main__":
    app()
