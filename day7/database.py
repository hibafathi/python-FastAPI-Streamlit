import sqlite3
DB_FILE = "app.db"
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT DEFAULT 'low'
            )
        ''')
        conn.commit()
        print("Database initialized.")
def add_task(title, priority):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (title, priority) VALUES (?, ?)', (title, priority))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute('SELECT * FROM users WHERE id = ?', (new_id,))
        row= cursor.fetchone()
        return dict(row)
def get_tasks():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        return [dict(row) for row in cursor.fetchall()]