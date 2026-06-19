import sqlite3

def setup():
    with sqlite3.connect("school.db") as conn:
        # create table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT NOT NULL,
                marks INTEGER NOT NULL
            )
        """)

        # insert 5 students using a loop
        students = [
            ("Arjun",  85),
            ("Priya",  92),
            ("Rahul",  47),
            ("Nisha",  78),
            ("Vikram", 63),
        ]

        conn.executemany(
            "INSERT INTO students (name, marks) VALUES (?, ?)",
            students
        )
        conn.commit()
        print("✅ 5 students inserted")

setup()