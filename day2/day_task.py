import json
import datetime
from typing import Optional
EXPENSE_FILE ="expense.json"
LOG_FILE= "log.txt"
def load_expenses()->list:
    """load expenses from file. Return empty list if file missing."""
    try:
        with open(EXPENSE_FILE,"r")as f:
            return json.load(f)
    except FileNotFoundError:
        return[]
def save_expenses(expenses: list) -> None:
    """Save expenses list to JSON file."""
    with open(EXPENSE_FILE, "w") as f:
        json.dump(expenses, f, indent=2)
def log_call(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # log to console
        print(f"  📝 LOG: {func.__name__} called | args={args} | kwargs={kwargs}")

        # log to file
        with open(LOG_FILE, "a") as f:
            f.write(
                f"[{timestamp}] FUNCTION={func.__name__} | "
                f"args={args} | kwargs={kwargs}\n"
            )

        result = func(*args, **kwargs)
        return result
    return wrapper
@log_call
def add_expense(category: str, amount: float) -> None:
    """Add a new expense and save to file."""
    expenses = load_expenses()

    expense = {
        "category": category.lower().strip(),
        "amount": amount,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(f"  ✅ Added: {category} — ₹{amount}")


@log_call
def get_summary() -> dict:
    """Return total spent per category."""
    expenses = load_expenses()

    if not expenses:
        print("  No expenses yet.")
        return {}

    summary = {}
    for exp in expenses:
        cat = exp["category"]
        summary[cat] = summary.get(cat, 0) + exp["amount"]

    print("\n  📊 Summary:")
    print("  " + "─" * 25)
    for category, total in sorted(summary.items()):
        print(f"  {category:<15} ₹{total:.2f}")
    print("  " + "─" * 25)
    total_all = sum(summary.values())
    print(f"  {'TOTAL':<15} ₹{total_all:.2f}")

    return summary


@log_call
def view_all() -> None:
    """Print all expenses."""
    expenses = load_expenses()

    if not expenses:
        print("  No expenses yet.")
        return

    print(f"\n  📋 All Expenses ({len(expenses)} records):")
    print("  " + "─" * 40)
    for i, exp in enumerate(expenses, 1):
        print(f"  {i}. [{exp['date']}] "
              f"{exp['category']:<12} ₹{exp['amount']:.2f}")
    print("  " + "─" * 40)
def read_logs() -> None:
    """Read log.txt and count how many times each function was called."""
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("  No logs yet.")
        return

    # count calls per function
    counts = {}
    for line in lines:
        # extract function name from log line
        # line format: [timestamp] FUNCTION=add_expense | args=...
        if "FUNCTION=" in line:
            func_name = line.split("FUNCTION=")[1].split(" |")[0]
            counts[func_name] = counts.get(func_name, 0) + 1

    print("\n  📈 Function Call Log:")
    print("  " + "─" * 25)
    for func, count in counts.items():
        print(f"  {func:<20} called {count} time(s)")
    print("  " + "─" * 25)
    print(f"  Total log entries: {len(lines)}")
def show_menu() -> None:
    print("\n" + "═" * 35)
    print("       EXPENSE TRACKER")
    print("═" * 35)
    print("  1. Add expense")
    print("  2. View summary")
    print("  3. View all expenses")
    print("  4. View logs")
    print("  5. Exit")
    print("═" * 35)

def main() -> None:
    print("💰 Welcome to Expense Tracker")

    while True:
        show_menu()
        choice = input("  Choose option: ").strip()

        # ── Add expense ───────────────────
        if choice == "1":
            category = input("  Category (food/transport/etc): ").strip()
            if not category:
                print("  ❌ Category cannot be empty")
                continue
            try:
                amount = float(input("  Amount (₹): "))
                if amount <= 0:
                    print("  ❌ Amount must be positive")
                    continue
                add_expense(category, amount)
            except ValueError:
                print("  ❌ Please enter a valid number")

        # ── Summary ───────────────────────
        elif choice == "2":
            get_summary()

        # ── View all ──────────────────────
        elif choice == "3":
            view_all()

        # ── View logs ─────────────────────
        elif choice == "4":
            read_logs()

        # ── Exit ──────────────────────────
        elif choice == "5":
            print("\n  Goodbye! 👋")
            break

        else:
            print("  ❌ Invalid option. Choose 1–5")

main()


