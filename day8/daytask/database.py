import sqlite3

DB_FILE = "app.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                email           TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT,
                priority    TEXT DEFAULT 'low',
                completed   INTEGER DEFAULT 0,
                owner_email TEXT NOT NULL
            )
        """)
        conn.commit()
    print("Database ready")

def db_get_user_by_email(email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

def db_create_user(email, hashed_password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, hashed_password) VALUES (?, ?)",
            (email, hashed_password)
        )
        conn.commit()
        return cursor.lastrowid

def db_create_task(data, owner_email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, priority, completed, owner_email) VALUES (?, ?, ?, ?, ?)",
            (
                data["title"],
                data.get("description"),
                data.get("priority", "low"),
                1 if data.get("completed", False) else 0,
                owner_email
            )
        )
        conn.commit()
        return db_get_task(cursor.lastrowid)

def db_get_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def db_get_tasks_by_owner(owner_email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE owner_email = ? ORDER BY id",
            (owner_email,)
        )
        return [dict(row) for row in cursor.fetchall()]

def db_get_task_for_owner(task_id, owner_email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE id = ? AND owner_email = ?",
            (task_id, owner_email)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

def db_update_task(task_id, data, owner_email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title=?, description=?, priority=?, completed=? WHERE id=? AND owner_email=?",
            (
                data["title"],
                data.get("description"),
                data.get("priority", "low"),
                1 if data.get("completed", False) else 0,
                task_id,
                owner_email
            )
        )
        conn.commit()
        if cursor.rowcount == 0:
            return None
        return db_get_task(task_id)

def db_delete_task(task_id, owner_email):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM tasks WHERE id = ? AND owner_email = ?",
            (task_id, owner_email)
        )
        conn.commit()
        return cursor.rowcount > 0