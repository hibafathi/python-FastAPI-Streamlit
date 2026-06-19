import sqlite3

DB_FILE = "students.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT    NOT NULL,
                marks INTEGER NOT NULL
            )
        """)
        conn.commit()

def insert_student(name: str, marks: int) -> dict:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (name, marks) VALUES (?, ?)",
            (name, marks)
        )
        conn.commit()
        return {"id": cursor.lastrowid, "name": name, "marks": marks}

def get_all_students() -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY id")
        return [dict(row) for row in cursor.fetchall()]

def get_student_by_id(student_id: int) -> dict | None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

def update_marks(student_id: int, new_marks: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE students SET marks = ? WHERE id = ?",
            (new_marks, student_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_student(student_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )
        conn.commit()
        return cursor.rowcount > 0

def get_students_above(threshold: int) -> list[dict]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM students WHERE marks > ? ORDER BY marks DESC",
            (threshold,)
        )
        return [dict(row) for row in cursor.fetchall()]

def print_student(student: dict) -> None:
    print(f"  [{student['id']}] {student['name']:<15} Marks: {student['marks']}")

def print_all(students: list[dict]) -> None:
    if not students:
        print("No students found.")
        return
    print(f"  {'ID':<5} {'Name':<15} {'Marks'}")
    print("  " + "-" * 30)
    for s in students:
        print_student(s)
    print("  " + "-" * 30)

def show_menu() -> None:
    print("\n" + "=" * 35)
    print("      STUDENT DATABASE")
    print("=" * 35)
    print("  1. Add student")
    print("  2. View all students")
    print("  3. View student by ID")
    print("  4. Update marks")
    print("  5. Delete student")
    print("  6. Students above threshold")
    print("  7. Exit")
    print("=" * 35)

def main() -> None:
    create_table()
    while True:
        show_menu()
        choice = input("  Choose option: ").strip()
        if choice == "1":
            name = input("  Name: ").strip()
            if not name:
                print("  Name cannot be empty")
                continue
            try:
                marks = int(input("  Marks (0-100): "))
                if not 0 <= marks <= 100:
                    print("  Marks must be between 0 and 100")
                    continue
                student = insert_student(name, marks)
                print(f"  Added: {student}")
            except ValueError:
                print("  Enter valid marks")
        elif choice == "2":
            students = get_all_students()
            print_all(students)
        elif choice == "3":
            try:
                sid = int(input("  Student ID: "))
                student = get_student_by_id(sid)
                if student:
                    print_student(student)
                else:
                    print(f"  Student {sid} not found")
            except ValueError:
                print("  Enter valid ID")
        elif choice == "4":
            try:
                sid = int(input("  Student ID: "))
                marks = int(input("  New marks (0-100): "))
                if not 0 <= marks <= 100:
                    print("  Marks must be between 0 and 100")
                    continue
                if update_marks(sid, marks):
                    print(f"  Marks updated for student {sid}")
                else:
                    print(f"  Student {sid} not found")
            except ValueError:
                print("  Enter valid numbers")
        elif choice == "5":
            try:
                sid = int(input("  Student ID: "))
                if delete_student(sid):
                    print(f"  Student {sid} deleted")
                else:
                    print(f"  Student {sid} not found")
            except ValueError:
                print("  Enter valid ID")
        elif choice == "6":
            try:
                threshold = int(input("  Minimum marks: "))
                students = get_students_above(threshold)
                print(f"  Students with marks above {threshold}:")
                print_all(students)
            except ValueError:
                print("  Enter valid number")
        elif choice == "7":
            print("  Goodbye")
            break
        else:
            print("  Invalid option. Choose 1-7")

main()