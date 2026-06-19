import sqlite3

DB_FILE = "app.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT,
                priority    TEXT DEFAULT 'low',
                completed   INTEGER DEFAULT 0
            )
        """)
        conn.commit()
    print("Database ready")

def db_get_all_tasks(status: str = None) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        if status == "done":
            cursor.execute(
                "SELECT * FROM tasks WHERE completed = ? ORDER BY id",
                (1,)
            )
        elif status == "pending":
            cursor.execute(
                "SELECT * FROM tasks WHERE completed = ? ORDER BY id",
                (0,)
            )
        else:
            cursor.execute("SELECT * FROM tasks ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]

def db_get_task(task_id: int) -> dict | None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

def db_create_task(data: dict) -> dict:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, priority, completed) VALUES (?, ?, ?, ?)",
            (
                data["title"],
                data.get("description"),
                data.get("priority", "low"),
                1 if data.get("completed", False) else 0
            )
        )
        conn.commit()
        return db_get_task(cursor.lastrowid)

def db_update_task(task_id: int, data: dict) -> dict | None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, priority = ?, completed = ? WHERE id = ?",
            (
                data["title"],
                data.get("description"),
                data.get("priority", "low"),
                1 if data.get("completed", False) else 0,
                task_id
            )
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return db_get_task(task_id)

def db_partial_update(task_id: int, data: dict) -> dict | None:
    existing = db_get_task(task_id)
    if existing is None:
        return None
    merged = {
        "title":       data.get("title")       or existing["title"],
        "description": data.get("description") or existing["description"],
        "priority":    data.get("priority")    or existing["priority"],
        "completed":   data.get("completed") if data.get("completed") is not None else bool(existing["completed"]),
    }
    return db_update_task(task_id, merged)

def db_delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0