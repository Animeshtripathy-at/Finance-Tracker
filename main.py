import sys
from database import (
    init_db,
    get_default_user_id,
    add_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
    get_balance_summary,
    get_category_expenses
)

def print_separator():
    print("-" * 50)

def display_menu():
    print_separator()
    print("Welcome to Personal Finance Tracker")
    print_separator()
    print("1. Add a Transaction")
    print("2. View Transactions")
    print("3. Update a Transaction")
    print("4. Delete a Transaction")
    print("5. View Balance Summary")
    print("6. View Category Expenses Report")
    print("7. Exit")
    print_separator()

def prompt_float(prompt: str) -> float:
    while True:
        try:
            val = float(input(prompt))
            if val < 0:
                print("Amount cannot be negative. Please try again.")
            else:
                return val
        except ValueError:
            print("Invalid input. Please enter a number.")

def handle_add_transaction(user_id: int):
    t_type = input("Enter Type (Income/Expense): ").strip().lower()
    if t_type not in ['income', 'expense']:
        print("Invalid type. Must be 'income' or 'expense'.")
        return
        
    category = input("Enter Category (e.g., Salary, Groceries, Rent): ").strip()
    amount = prompt_float("Enter Amount: ")
    description = input("Enter Description (Optional): ").strip()
    date = input("Enter Date (YYYY-MM-DD) or press Enter for today: ").strip()
    
    date_val = date if date else None
    
    t_id = add_transaction(user_id, t_type, category, amount, description, date_val)
    print(f"Transaction successfully added with ID: {t_id}")

def handle_view_transactions(user_id: int):
    transactions = get_transactions(user_id)
    if not transactions:
        print("No transactions found.")
        return
        
    print(f"\n{'ID':<5} | {'Date':<10} | {'Type':<8} | {'Category':<15} | {'Amount ($)':<10} | {'Description'}")
    print("-" * 75)
    for t in transactions:
        print(f"{t['id']:<5} | {t['date']:<10} | {t['type'].title():<8} | {t['category']:<15} | ${t['amount']:<9.2f} | {t['description']}")

def handle_update_transaction(user_id: int):
    handle_view_transactions(user_id)
    try:
        t_id = int(input("\nEnter the ID of the transaction to update: "))
    except ValueError:
        print("Invalid ID.")
        return
        
    print("Enter the new details.")
    category = input("Enter New Category: ").strip()
    amount = prompt_float("Enter New Amount: ")
    description = input("Enter New Description (Optional): ").strip()
    date = input("Enter New Date (YYYY-MM-DD): ").strip()
    
    if update_transaction(t_id, user_id, category, amount, description, date):
        print("Transaction updated successfully.")
    else:
        print("Update failed. Please check the Transaction ID format.")

def handle_delete_transaction(user_id: int):
    handle_view_transactions(user_id)
    try:
        t_id = int(input("\nEnter the ID of the transaction to delete: "))
        
        # We don't have delete functionality inside the main module, 
        # so let's check it handles deletion from db module correctly
        if delete_transaction(t_id, user_id):
            print("Transaction deleted successfully.")
        else:
             print("Delete failed. Please check the Transaction ID format.")
             
    except ValueError:
        print("Invalid ID.")

def handle_view_summary(user_id: int):
    summary = get_balance_summary(user_id)
    print("\n--- Balance Summary ---")
    print(f"Total Income:  ${summary['total_income']:.2f}")
    print(f"Total Expense: ${summary['total_expense']:.2f}")
    print(f"Net Balance:   ${summary['balance']:.2f}")

def handle_category_report(user_id: int):
    expenses = get_category_expenses(user_id)
    if not expenses:
        print("\nNo expenses to summarize.")
        return
        
    print("\n--- Category-wise Expenses ---")
    print(f"{'Category':<20} | {'Total Spent ($)'}")
    print("-" * 40)
    for e in expenses:
        print(f"{e['category']:<20} | ${e['total']:<15.2f}")

def main():
    # Setup DB and get default user session
    init_db()
    user_id = get_default_user_id()
    if not user_id:
        print("System error: Default user not initialized.")
        sys.exit(1)
        
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            handle_add_transaction(user_id)
        elif choice == '2':
            handle_view_transactions(user_id)
        elif choice == '3':
            handle_update_transaction(user_id)
        elif choice == '4':
            handle_delete_transaction(user_id)
        elif choice == '5':
            handle_view_summary(user_id)
        elif choice == '6':
            handle_category_report(user_id)
        elif choice == '7':
            print("Exiting Personal Finance Tracker. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select an option from 1 to 7.")

if __name__ == "__main__":
    main()
