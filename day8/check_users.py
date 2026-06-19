import sqlite3

conn = sqlite3.connect("app.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(f"ID    : {row['id']}")
    print(f"Email : {row['email']}")
    print(f"Hash  : {row['hashed_password']}")
    print("-" * 40)

conn.close()
