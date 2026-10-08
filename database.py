import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

DB_NAME = "finance_tracker.db"

def get_connection(db_name: str = DB_NAME) -> sqlite3.Connection:
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # To return dictionary-like rows
    return conn

def init_db(db_name: str = DB_NAME):
    """Initializes the database schema."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        
        # Create Users table (for future extensibility, even if single user now)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount >= 0),
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Ensure at least one default user exists
        cursor.execute('SELECT COUNT(*) FROM users')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO users (username) VALUES (?)', ('default_user',))
            
        conn.commit()
    finally:
        conn.close()

# --- CRUD Operations ---

def add_transaction(user_id: int, t_type: str, category: str, amount: float, description: str, date: Optional[str] = None, db_name: str = DB_NAME) -> int:
    """Adds a new transaction and returns its ID."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        
        if date is None:
            # Use current date (YYYY-MM-DD) if none provided
            date = datetime.now().strftime("%Y-%m-%d")
            
        cursor.execute('''
            INSERT INTO transactions (user_id, type, category, amount, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, t_type.lower(), category, amount, description, date))
        
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_transactions(user_id: int, db_name: str = DB_NAME) -> List[Dict]:
    """Retrieves all transactions for a specific user."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, type, category, amount, description, date 
            FROM transactions 
            WHERE user_id = ?
            ORDER BY date DESC, id DESC
        ''', (user_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def update_transaction(transaction_id: int, user_id: int, category: str, amount: float, description: str, date: str, db_name: str = DB_NAME) -> bool:
    """Updates an existing transaction. Returns True if successful."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE transactions
            SET category = ?, amount = ?, description = ?, date = ?
            WHERE id = ? AND user_id = ?
        ''', (category, amount, description, date, transaction_id, user_id))
        
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def delete_transaction(transaction_id: int, user_id: int, db_name: str = DB_NAME) -> bool:
    """Deletes a transaction. Returns True if successful."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?', (transaction_id, user_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

# --- Reporting Queries ---

def get_balance_summary(user_id: int, db_name: str = DB_NAME) -> Dict[str, float]:
    """Returns the total income, total expense, and current balance."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
            FROM transactions
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        
        # Handle cases where table is empty (SUM returns None)
        income = row['total_income'] or 0.0
        expense = row['total_expense'] or 0.0
        balance = income - expense
        
        return {
            'total_income': income,
            'total_expense': expense,
            'balance': balance
        }
    finally:
        conn.close()

def get_category_expenses(user_id: int, db_name: str = DB_NAME) -> List[Dict]:
    """Returns total expenses grouped by category."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE user_id = ? AND type = 'expense'
            GROUP BY category
            ORDER BY total DESC
        ''', (user_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def get_default_user_id(db_name: str = DB_NAME) -> Optional[int]:
    """Helper to get the ID of the default user."""
    conn = get_connection(db_name)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = 'default_user'")
        row = cursor.fetchone()
        return row['id'] if row else None
    finally:
        conn.close()

if __name__ == "__main__":
    # Test initialization
    init_db()
    print("Database initialized successfully.")
