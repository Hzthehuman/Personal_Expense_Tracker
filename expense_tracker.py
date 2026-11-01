import json
import os
from datetime import datetime
from collections import defaultdict


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

# Define the JSON file used to store transaction records
FILE_NAME = "expenses.json"

# List of available expense categories
CATEGORIES = [
    "Food",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Education",
    "Health",
    "Bills",
    "Others"
]


# ==========================================
# 2. DATA STORAGE
# ==========================================

def load_transactions():
    # Load previously saved transactions from the JSON file

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Make sure the loaded data is in list format
        if not isinstance(data, list):
            print("Invalid data format. Starting with empty records.")
            return []

        return data

    except (json.JSONDecodeError, OSError):
        # Handle missing, corrupted, or unreadable data
        print("Unable to load data. Starting with empty records.")
        return []


def save_transactions(transactions):
    # Save all transaction records to the JSON file

    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

    except OSError:
        print("Error: Unable to save transactions.")


# ==========================================
# 3. INPUT VALIDATION
# ==========================================

def get_amount():
    # Accept only valid positive numerical values

    while True:
        try:
            amount = float(input("Enter amount: "))

            # Prevent zero, negative, and infinite amounts
            if amount <= 0 or not __import__("math").isfinite(amount):
                print("Amount must be a valid positive number.")
                continue

            return round(amount, 2)

        except ValueError:
            # Ask again if the user enters non-numeric input
            print("Invalid amount. Please enter a number.")


def get_date():
    # Allow users to enter a custom transaction date

    while True:
        date = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        ).strip()

        # Use today's date when the user leaves the input empty
        if not date:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            # Validate and format the entered date
            return datetime.strptime(
                date, "%Y-%m-%d"
            ).strftime("%Y-%m-%d")

        except ValueError:
            print("Invalid date format. Example: 2026-11-01")


# ==========================================
# 4. TRANSACTION MANAGEMENT
# ==========================================

def add_transaction(transactions, transaction_type):

    print(f"\n--- Add {transaction_type} ---")

    # Collect transaction information
    amount = get_amount()

    description = input("Enter description: ").strip()

    if not description:
        description = "No description"

    date = get_date()

    # Assign a category to expense transactions
    if transaction_type == "Expense":

        print("\nAvailable Categories:")

        for index, category in enumerate(CATEGORIES, 1):
            print(f"{index}. {category}")

        while True:
            try:
                choice = int(input("Select category: "))

                if 1 <= choice <= len(CATEGORIES):
                    category = CATEGORIES[choice - 1]
                    break

                print("Please select a valid category.")

            except ValueError:
                print("Please enter a valid number.")

    else:
        category = "Income"

    # Create a dictionary to store transaction details
    transaction = {
        "id": len(transactions) + 1,
        "type": transaction_type,
        "amount": amount,
        "description": description,
        "category": category,
        "date": date
    }

    # Add the new transaction to the records
    transactions.append(transaction)

    # Automatically save updated records
    save_transactions(transactions)

    print("\nTransaction added successfully!")


# ==========================================
# 5. VIEW TRANSACTIONS
# ==========================================

def view_transactions(transactions):

    print("\n========== ALL TRANSACTIONS ==========")

    if not transactions:
        print("No transactions found.")
        return

    # Display transaction information in columns
    print(
        f"{'ID':<5} {'Type':<10} {'Amount':>12} "
        f"{'Category':<17} {'Date':<12}"
    )

    print("-" * 65)

    for item in transactions:

        print(
            f"{item['id']:<5} "
            f"{item['type']:<10} "
            f"{item['amount']:>12,.2f} "
            f"{item['category']:<17} "
            f"{item['date']:<12}"
        )

        print(f"      Description: {item['description']}")


# ==========================================
# 6. FINANCIAL SUMMARY
# ==========================================

def financial_summary(transactions):

    # Calculate total income from all income records
    total_income = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "Income"
    )

    # Calculate total expenses from all expense records
    total_expense = sum(
        item["amount"]
        for item in transactions
        if item["type"] == "Expense"
    )

    # Calculate remaining balance
    balance = total_income - total_expense

    print("\n========== FINANCIAL SUMMARY ==========")

    print(f"Total Income   : {total_income:,.2f}")
    print(f"Total Expenses : {total_expense:,.2f}")
    print(f"Current Balance: {balance:,.2f}")

    print("=" * 40)


# ==========================================
# 7. SEARCH TRANSACTIONS
# ==========================================

def search_transactions(transactions):

    # Search records using a description keyword
    keyword = input(
        "\nEnter description to search: "
    ).strip().lower()

    # Find matching descriptions without case sensitivity
    results = [
        item for item in transactions
        if keyword in item["description"].lower()
    ]

    print("\n========== SEARCH RESULTS ==========")

    if results:
        view_transactions(results)
    else:
        print("No matching transactions found.")


# ==========================================
# 8. FILTER BY CATEGORY
# ==========================================

def filter_by_category(transactions):

    print("\nAvailable Categories:")

    for index, category in enumerate(CATEGORIES, 1):
        print(f"{index}. {category}")

    try:
        choice = int(input("Select category: "))

        if not 1 <= choice <= len(CATEGORIES):
            print("Invalid category.")
            return

        selected = CATEGORIES[choice - 1]

        # Filter transactions based on the selected category
        results = [
            item for item in transactions
            if item["category"] == selected
        ]

        print(f"\nTransactions in {selected}:")

        if results:
            view_transactions(results)
        else:
            print("No transactions in this category.")

    except ValueError:
        print("Invalid input.")


# ==========================================
# 9. DELETE TRANSACTION
# ==========================================

def delete_transaction(transactions):

    # Display records before asking which one to delete
    view_transactions(transactions)

    if not transactions:
        return

    try:
        transaction_id = int(
            input("\nEnter transaction ID to delete: ")
        )

        for item in transactions:

            if item["id"] == transaction_id:

                # Confirm deletion before removing a record
                confirmation = input(
                    "Are you sure? (yes/no): "
                ).strip().lower()

                if confirmation == "yes":

                    transactions.remove(item)

                    # Reassign IDs to maintain sequential numbering
                    for index, record in enumerate(
                        transactions, 1
                    ):
                        record["id"] = index

                    # Save the updated transaction list
                    save_transactions(transactions)

                    print("Transaction deleted successfully!")

                else:
                    print("Deletion cancelled.")

                return

        print("Transaction ID not found.")

    except ValueError:
        print("Invalid ID.")


# ==========================================
# 10. MONTHLY EXPENSE REPORT
# ==========================================

def monthly_report(transactions):

    # Ask the user which month they want to review
    month = input(
        "\nEnter month (YYYY-MM): "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")

    except ValueError:
        print("Invalid format. Example: 2026-11")
        return

    # Select transactions belonging to the chosen month
    monthly_data = [
        item for item in transactions
        if item["date"].startswith(month)
    ]

    if not monthly_data:
        print("No transactions found for this month.")
        return

    # Calculate monthly income and expenses
    income = sum(
        item["amount"] for item in monthly_data
        if item["type"] == "Income"
    )

    expenses = sum(
        item["amount"] for item in monthly_data
        if item["type"] == "Expense"
    )

    # Group expenses by category for a spending breakdown
    category_totals = defaultdict(float)

    for item in monthly_data:

        if item["type"] == "Expense":
            category_totals[item["category"]] += item["amount"]

    print(f"\n========== MONTHLY REPORT: {month} ==========")

    print(f"Total Income  : {income:,.2f}")
    print(f"Total Expenses: {expenses:,.2f}")
    print(f"Net Balance   : {income - expenses:,.2f}")

    print("\nExpense Breakdown:")

    if category_totals:
        for category, amount in category_totals.items():
            print(f"{category:<20}: {amount:,.2f}")
    else:
        print("No expenses recorded.")

    print("=" * 45)


# ==========================================
# 11. MAIN MENU
# ==========================================

def display_menu():

    # Show all available application features
    print("\n" + "=" * 45)
    print("         PERSONAL EXPENSE TRACKER")
    print("=" * 45)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Transactions")
    print("4. Financial Summary")
    print("5. Search Transactions")
    print("6. Filter by Category")
    print("7. Delete Transaction")
    print("8. Monthly Expense Report")
    print("9. Exit")

    print("=" * 45)


# ==========================================
# 12. MAIN APPLICATION
# ==========================================

def main():

    # Load saved transactions when the application starts
    transactions = load_transactions()

    print("\nWelcome to Personal Expense Tracker!")

    # Keep the application running until the user exits
    while True:

        display_menu()

        choice = input("Choose an option (1-9): ").strip()

        # Execute the selected application feature
        if choice == "1":
            add_transaction(transactions, "Income")

        elif choice == "2":
            add_transaction(transactions, "Expense")

        elif choice == "3":
            view_transactions(transactions)

        elif choice == "4":
            financial_summary(transactions)

        elif choice == "5":
            search_transactions(transactions)

        elif choice == "6":
            filter_by_category(transactions)

        elif choice == "7":
            delete_transaction(transactions)

        elif choice == "8":
            monthly_report(transactions)

        elif choice == "9":
            # Save records before closing the application
            save_transactions(transactions)
            print("\nThank you for using Expense Tracker!")
            break

        else:
            print("Invalid option. Please try again.")


# ==========================================
# 13. PROGRAM ENTRY POINT
# ==========================================

# Run the main application when this file is executed directly
if __name__ == "__main__":
    main()
