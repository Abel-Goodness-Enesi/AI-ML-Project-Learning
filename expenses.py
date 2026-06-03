import csv 
import os 
import argparse
from datetime import date

FILE =  "expenses.csv"
HEADERS = ["id", "date", "amount", "category", "description"]

def init_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()

def add_expense(amount, category, description, expense_date=None):
    init_file()

    expenses = load_expenses()
    new_id = max([int(e["id"]) for e in expenses], default=0) + 1
    with open(FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow({
            "id" : new_id,
            "date": expense_date if expense_date else date.today(), 
            "amount": amount, 
            "category": category,
            "description": description
        })

    print(f"Added expense {category} of #{amount} id:{new_id} ")

def load_expenses():
    init_file()

    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)
    

def view_expenses(month=None):
    expenses = load_expenses()
    if not expenses:
        print("No expense is yet to be added")
        return
    print(f"\n {"ID":<5} {"Date":<12} {"Amount":<12} {"Category":<12} {"Description":<15}")
    print("-"*60)

    for e in expenses:
        print(f"{e['id']:<5} {e['date']:<12} {e['amount']:<12} {e['category']:<12} {e['description']:<15}")
    print("-"*60)

    total = sum(float(e["amount"]) for e in expenses)
    print("-"*35)
    print(f"{'Total':<30}is #{total:2f}")

def summarise():
    expenses = load_expenses()

    if not expenses:
        print("No expense to summarise.")
        return 
    
    total = {}
    for e in expenses:
        cat = e["category"]
        total[cat] = total.get(cat, 0) + float(e["amount"])

    for cat, total in sorted(total.items(), key=lambda x: x[1], reverse=True):
        print(f"{cat:<20} #{total:.2f}")

def delete_expense(expense_id):
    expenses = load_expenses()
    original_count = len(expenses)

    expenses = [e for e in expenses if e["id"] != str(expense_id)]

    if original_count == len(expenses):
        print(f"No expense with that {expense_id} is found")
        return 
    
    with open(FILE, "w", newline="") as f:
        writer= csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(expenses)


def main():
    parser = argparse.ArgumentParser(description="Smart Expense Tracker")
    subparser = parser.add_subparsers(dest="command")

    add_parser = subparser.add_parser("add", help="Add an expense")
    add_parser.add_argument("amount", type=float, help="Enter in an amount in Naira #")
    add_parser.add_argument("category", help="Category(food, transport)")
    add_parser.add_argument("description", help="rice and stew")
    add_parser.add_argument("--date", help="Date of expense entry")
    view_parser = subparser.add_parser("view", help="To view an expense")
    view_parser.add_argument("--month",)

    subparser.add_parser("summary", help="To give a summary of expenses")

    del_parser = subparser.add_parser("delete", help="To delete an expense")
    del_parser.add_argument("id", type=int, help="Enter the expense id")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.category, args.description, args.date)

    elif args.command == "view":
        view_expenses(args.month)

    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        summarise()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()