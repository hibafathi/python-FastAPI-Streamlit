import json
import datetime
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional

EXPENSES_FILE = "expenses.json"
LOG_FILE      = "log.txt"
class Expense(BaseModel):
    category: str
    amount:   float
    date:     Optional[str] = None   # auto-filled below

    @field_validator("category")
    def category_must_not_be_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Category cannot be empty")
        return value.lower()         # always lowercase

    @field_validator("amount")
    def amount_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Amount must be greater than zero")
        return value
def load_expenses() -> list[dict]:
    try:
        with open(EXPENSES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_expenses(expenses: list[dict]) -> None:
    with open(EXPENSES_FILE, "w") as f:
        json.dump(expenses, f, indent=2)
def log_call(func):
    def wrapper(*args, **kwargs):
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  📝 LOG: {func.__name__} called "
              f"| args={args} | kwargs={kwargs}")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] FUNCTION={func.__name__} | "
                    f"args={args} | kwargs={kwargs}\n")
        return func(*args, **kwargs)
    return wrapper
@log_call
def add_expense(category: str, amount: float) -> None:
    """Validate with Pydantic then save to file."""
    try:
        expense_obj = Expense(
            category=category,
            amount=amount,
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    except ValidationError as e:
        # extract clean error messages
        for error in e.errors():
            print(f"  ❌ Validation Error — {error['loc'][0]}: {error['msg']}")
        return  
    expense_dict: dict = expense_obj.model_dump()
    expenses: list[dict] = load_expenses()
    expenses.append(expense_dict)
    save_expenses(expenses)

    print(f"  ✅ Saved: {expense_obj.category} — ₹{expense_obj.amount:.2f}")
@log_call
def get_summary() -> dict[str, float]:
    expenses: list[dict] = load_expenses()

    if not expenses:
        print("  No expenses yet.")
        return {}

    summary: dict[str, float] = {}
    for exp in expenses:
        cat: str = exp["category"]
        summary[cat] = summary.get(cat, 0.0) + exp["amount"]

    print("\n  📊 Summary:")
    print("  " + "─" * 25)
    for category, total in sorted(summary.items()):
        print(f"  {category:<15} ₹{total:.2f}")
    print("  " + "─" * 25)
    total_all: float = sum(summary.values())
    print(f"  {'TOTAL':<15} ₹{total_all:.2f}")

    return summary
@log_call
def view_all() -> None:
    expenses: list[dict] = load_expenses()

    if not expenses:
        print("  No expenses yet.")
        return

    print(f"\n  📋 All Expenses ({len(expenses)} records):")
    print("  " + "─" * 40)
    for i, exp in enumerate(expenses, 1):
        print(f"  {i}. [{exp['date']}] "
              f"{exp['category']:<12} ₹{exp['amount']:.2f}")
    print("  " + "─" * 40)
def read_logs() -> dict[str, int]:
    try:
        with open(LOG_FILE, "r") as f:
            lines: list[str] = f.readlines()
    except FileNotFoundError:
        print("  No logs yet.")
        return {}

    counts: dict[str, int] = {}
    for line in lines:
        if "FUNCTION=" in line:
            func_name: str = line.split("FUNCTION=")[1].split(" |")[0]
            counts[func_name] = counts.get(func_name, 0) + 1

    print("\n  📈 Function Call Log:")
    print("  " + "─" * 25)
    for func, count in counts.items():
        print(f"  {func:<20} called {count} time(s)")
    print("  " + "─" * 25)
    print(f"  Total log entries: {len(lines)}")
    return counts
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
        choice: str = input("  Choose option: ").strip()

        if choice == "1":
            category: str = input("  Category: ").strip()
            try:
                amount: float = float(input("  Amount (₹): "))
                add_expense(category, amount)
            except ValueError:
                print("  ❌ Please enter a valid number for amount")

        elif choice == "2":
            get_summary()

        elif choice == "3":
            view_all()

        elif choice == "4":
            read_logs()

        elif choice == "5":
            print("\n  Goodbye! 👋")
            break

        else:
            print("  ❌ Invalid option. Choose 1–5")

main()