# Personal Finance Tracker

A command-line based Personal Finance Tracker built with Python and SQLite. It allows you to manage income and expenses, viewing summaries and categorizing transactions.

## Features
- **Add Transactions:** Record incomes or expenses with details like category, amount, description, and date.
- **View Transactions:** See a list of your historical transactions.
- **Update Transactions:** Modify existing records if you made a mistake.
- **Delete Transactions:** Remove incorrect entries.
- **Balance Summary:** View your total income, total expenses, and current net balance.
- **Category-wise Report:** Analyze where your money goes with an ordered summary of expenses by category.

## Requirements
- Python 3.7+

*Note: The application uses the built-in `sqlite3` driver, so no extra database server is needed.*

## Installation & Setup

1. **Clone or Download the Repository**
2. **Navigate to the Directory:**
   ```bash
   cd "finance tracker"
   ```
3. **(Optional) Run tests to verify the database Logic:**
   ```bash
   python -m unittest test_database.py
   ```

## Usage

Run the main application using Python:
```bash
python main.py
```

An interactive menu will appear on your terminal:
```
--------------------------------------------------
Welcome to Personal Finance Tracker
--------------------------------------------------
1. Add a Transaction
2. View Transactions
3. Update a Transaction
4. Delete a Transaction
5. View Balance Summary
6. View Category Expenses Report
7. Exit
--------------------------------------------------
```
Follow the on-screen prompts to manage your finances!
