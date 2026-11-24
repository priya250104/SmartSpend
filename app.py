
from datetime import date, datetime
from uuid import uuid4

from storage import (
    load_transactions,
    save_transactions,
    import_json_transactions
)

import_json_transactions()
transactions = load_transactions()


# Income categories
INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Pocket Money",
    "Investment",
    "Other"
]


# Expense categories
EXPENSE_CATEGORIES = [
    "Food",
    "Rent",
    "Groceries",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Healthcare",
    "Entertainment",
    "Travel",
    "Other"
]


# Display welcome message
def display_welcome():
    print("=" * 55)
    print("                    SMARTSPEND")
    print("             Personal Finance Tracker")
    print("=" * 55)
    print(f"Loaded {len(transactions)} saved transactions.")


# Get valid amount
def get_amount():
    while True:
        try:
            amount = float(input("Enter amount (₹): "))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return round(amount, 2)

        except ValueError:
            print("Please enter a valid number.")


# Select category
def select_category(transaction_type):
    categories = (
        INCOME_CATEGORIES
        if transaction_type == "Income"
        else EXPENSE_CATEGORIES
    )

    print("\nAvailable Categories:")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input("Select category number: "))

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid category number.")

        except ValueError:
            print("Please enter a valid number.")


# Get valid transaction date
def get_transaction_date():
    today = date.today()

    print(f"Today's date: {today}")
    print("Press Enter to use today's date.")

    while True:
        date_input = input("Enter date (YYYY-MM-DD): ").strip()

        if not date_input:
            return str(today)

        try:
            selected_date = datetime.strptime(
                date_input, "%Y-%m-%d"
            ).date()

            if selected_date > today:
                print("Future dates are not allowed.")
                continue

            return str(selected_date)

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")


# Add income or expense
def add_transaction(transaction_type):
    print(f"\n--- Add {transaction_type} ---")

    amount = get_amount()
    category = select_category(transaction_type)
    description = input("Enter description: ").strip()
    transaction_date = get_transaction_date()

    transaction = {
        "id": str(uuid4()).upper(),
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description or "No description",
        "date": transaction_date
    }

    transactions.append(transaction)
    save_transactions(transactions)

    print("\nTransaction added successfully!")
    print(f"Transaction ID: {transaction['id']}")


# Display transactions
def view_transactions(transaction_list=None):
    print("\n--- Transaction History ---")

    if transaction_list is None:
        transaction_list = transactions

    if not transaction_list:
        print("No transactions found.")
        return

    print("-" * 110)

    print(
        f"{'ID':<38} {'Date':<12} {'Type':<10} "
        f"{'Category':<15} {'Amount':>12} {'Description':<20}"
    )

    print("-" * 110)

    for transaction in transaction_list:
        print(
            f"{transaction['id']:<38} "
            f"{transaction['date']:<12} "
            f"{transaction['type']:<10} "
            f"{transaction['category']:<15} "
            f"₹{transaction['amount']:>10.2f} "
            f"{transaction['description']:<20}"
        )

    print("-" * 110)


# Search transaction
def search_transaction():
    print("\n--- Search Transaction ---")

    search_id = input("Enter Transaction ID: ").strip().upper()

    for transaction in transactions:
        if transaction["id"].upper() == search_id:
            print("\nTransaction Found!")
            view_transactions([transaction])
            return

    print("Transaction not found.")


# Find transaction by ID
def find_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"].upper() == transaction_id.upper():
            return transaction

    return None


# Edit transaction
def edit_transaction():
    print("\n--- Edit Transaction ---")

    transaction_id = input("Enter Transaction ID: ").strip()
    transaction = find_transaction(transaction_id)

    if transaction is None:
        print("Transaction not found.")
        return

    print("\nCurrent Transaction:")
    view_transactions([transaction])

    print("\nWhat would you like to edit?")
    print("1. Amount")
    print("2. Category")
    print("3. Description")
    print("4. Date")
    print("5. Transaction Type")
    print("6. Cancel")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        transaction["amount"] = get_amount()

    elif choice == "2":
        transaction["category"] = select_category(
            transaction["type"]
        )

    elif choice == "3":
        description = input("Enter new description: ").strip()

        if description:
            transaction["description"] = description
        else:
            print("Description cannot be empty.")
            return

    elif choice == "4":
        transaction["date"] = get_transaction_date()

    elif choice == "5":
        print("1. Income")
        print("2. Expense")

        type_choice = input("Select transaction type: ").strip()

        if type_choice == "1":
            new_type = "Income"
        elif type_choice == "2":
            new_type = "Expense"
        else:
            print("Invalid choice.")
            return

        transaction["type"] = new_type
        transaction["category"] = select_category(new_type)

    elif choice == "6":
        print("Edit cancelled.")
        return

    else:
        print("Invalid choice.")
        return

    save_transactions(transactions)
    print("Transaction updated successfully!")


# Delete transaction
def delete_transaction():
    print("\n--- Delete Transaction ---")

    transaction_id = input("Enter Transaction ID: ").strip()
    transaction = find_transaction(transaction_id)

    if transaction is None:
        print("Transaction not found.")
        return

    print("\nTransaction to delete:")
    view_transactions([transaction])

    confirm = input(
        "Are you sure you want to delete? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        transactions.remove(transaction)
        save_transactions(transactions)
        print("Transaction deleted successfully!")

    else:
        print("Deletion cancelled.")


# Filter transactions
def filter_transactions():
    print("\n--- Filter Transactions ---")

    print("1. Filter by Type")
    print("2. Filter by Category")
    print("3. Filter by Date")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        print("1. Income")
        print("2. Expense")

        type_choice = input("Select type: ").strip()

        if type_choice == "1":
            selected_type = "Income"
        elif type_choice == "2":
            selected_type = "Expense"
        else:
            print("Invalid choice.")
            return

        filtered = [
            t for t in transactions
            if t["type"] == selected_type
        ]

    elif choice == "2":
        category = input("Enter category name: ").strip()

        filtered = [
            t for t in transactions
            if t["category"].lower() == category.lower()
        ]

    elif choice == "3":
        selected_date = get_transaction_date()

        filtered = [
            t for t in transactions
            if t["date"] == selected_date
        ]

    else:
        print("Invalid choice.")
        return

    print(f"\nFound {len(filtered)} transaction(s).")
    view_transactions(filtered)


# Sort transactions
def sort_transactions():
    print("\n--- Sort Transactions ---")

    print("1. Amount: Low to High")
    print("2. Amount: High to Low")
    print("3. Date: Oldest First")
    print("4. Date: Newest First")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        sorted_list = sorted(
            transactions,
            key=lambda t: t["amount"]
        )

    elif choice == "2":
        sorted_list = sorted(
            transactions,
            key=lambda t: t["amount"],
            reverse=True
        )

    elif choice == "3":
        sorted_list = sorted(
            transactions,
            key=lambda t: t["date"]
        )

    elif choice == "4":
        sorted_list = sorted(
            transactions,
            key=lambda t: t["date"],
            reverse=True
        )

    else:
        print("Invalid choice.")
        return

    view_transactions(sorted_list)


# Calculate total income
def calculate_total_income():
    total = sum(
        t["amount"] for t in transactions
        if t["type"] == "Income"
    )

    return round(total, 2)


# Calculate total expenses
def calculate_total_expenses():
    total = sum(
        t["amount"] for t in transactions
        if t["type"] == "Expense"
    )

    return round(total, 2)


# Calculate balance
def calculate_balance():
    return round(
        calculate_total_income() - calculate_total_expenses(),
        2
    )


# Display financial summary
def display_summary():
    income = calculate_total_income()
    expenses = calculate_total_expenses()
    balance = calculate_balance()

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Income   : ₹{income:.2f}")
    print(f"Total Expenses : ₹{expenses:.2f}")
    print(f"Balance        : ₹{balance:.2f}")

    if income > 0:
        savings_rate = (balance / income) * 100
        print(f"Savings Rate   : {savings_rate:.2f}%")
    else:
        print("Savings Rate   : N/A")

    print("=======================================")


# Display menu
def display_menu():
    print("\n------------- SMARTSPEND MENU -------------")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Total Income")
    print("5. View Total Expenses")
    print("6. View Balance")
    print("7. Financial Summary")
    print("8. Search Transaction")
    print("9. Edit Transaction")
    print("10. Delete Transaction")
    print("11. Filter Transactions")
    print("12. Sort Transactions")
    print("13. Exit")
    print("-------------------------------------------")


# Main application
def main():
    display_welcome()

    while True:
        display_menu()

        choice = input("Enter your choice (1-13): ").strip()

        if choice == "1":
            add_transaction("Income")

        elif choice == "2":
            add_transaction("Expense")

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            print(f"Total Income: ₹{calculate_total_income():.2f}")

        elif choice == "5":
            print(f"Total Expenses: ₹{calculate_total_expenses():.2f}")

        elif choice == "6":
            print(f"Balance: ₹{calculate_balance():.2f}")

        elif choice == "7":
            display_summary()

        elif choice == "8":
            search_transaction()

        elif choice == "9":
            edit_transaction()

        elif choice == "10":
            delete_transaction()

        elif choice == "11":
            filter_transactions()

        elif choice == "12":
            sort_transactions()

        elif choice == "13":
            print("\nThank you for using SmartSpend!")
            print("Your transactions are safely stored.")
            break

        else:
            print("Invalid choice! Please select from 1 to 13.")


if __name__ == "__main__":
    main()
