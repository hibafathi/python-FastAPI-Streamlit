import sqlite3
def delete_by_name(name: str) -> None:
    with sqlite3.connect("school.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM students WHERE name = ?",
            (name,)
        )
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ '{name}' deleted successfully")
        else:
            print(f"❌ '{name}' not found")
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        print("\nRemaining students:")
        for row in rows:
            print(f"  {row['id']}. {row['name']} — {row['marks']}")

delete_by_name("Rahul")