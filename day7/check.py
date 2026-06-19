import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"Tables in DB: {tables}")

if tables:
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    print(f"Total tasks: {len(rows)}")
    print("-" * 30)
    for row in rows:
        print(row)
else:
    print("No tables found in database")

conn.close()