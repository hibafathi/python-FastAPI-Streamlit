import sqlite3
def get_above_70():
    with sqlite3.connect("school.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE marks > ?",
            (70,)
        )
        rows = cursor.fetchall()

        print("\nStudents with marks above 70:")
        print("─" * 30)
        for row in rows:
            print(f"  {row['name']:<10} → {row['marks']}")

get_above_70()