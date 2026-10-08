import unittest
import sqlite3
import os
from database import (
    init_db,
    get_connection,
    add_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
    get_balance_summary,
    get_category_expenses,
    get_default_user_id
)

TEST_DB = "test_finance_tracker.db"

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Initialize test database
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        init_db(TEST_DB)
        self.user_id = get_default_user_id(TEST_DB)

    def tearDown(self):
        # Cleanup test database
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_add_transaction(self):
        t_id = add_transaction(self.user_id, 'income', 'Salary', 5000.0, 'Monthly salary', '2023-01-01', TEST_DB)
        self.assertIsNotNone(t_id)

        transactions = get_transactions(self.user_id, TEST_DB)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['category'], 'Salary')
        self.assertEqual(transactions[0]['amount'], 5000.0)

    def test_get_transactions(self):
        add_transaction(self.user_id, 'income', 'Salary', 1000.0, '', '2023-01-01', TEST_DB)
        add_transaction(self.user_id, 'expense', 'Food', 20.0, '', '2023-01-02', TEST_DB)
        
        transactions = get_transactions(self.user_id, TEST_DB)
        self.assertEqual(len(transactions), 2)
        # Should be ordered by date DESC
        self.assertEqual(transactions[0]['category'], 'Food')

    def test_update_transaction(self):
        t_id = add_transaction(self.user_id, 'expense', 'Groceries', 50.0, '', '2023-01-01', TEST_DB)
        
        # Update category and amount
        success = update_transaction(t_id, self.user_id, 'Supermarket', 60.0, 'Milk and Bread', '2023-01-01', TEST_DB)
        self.assertTrue(success)
        
        transactions = get_transactions(self.user_id, TEST_DB)
        self.assertEqual(transactions[0]['category'], 'Supermarket')
        self.assertEqual(transactions[0]['amount'], 60.0)
        self.assertEqual(transactions[0]['description'], 'Milk and Bread')

    def test_delete_transaction(self):
        t_id = add_transaction(self.user_id, 'expense', 'Coffee', 5.0, '', '2023-01-01', TEST_DB)
        
        success = delete_transaction(t_id, self.user_id, TEST_DB)
        self.assertTrue(success)
        
        transactions = get_transactions(self.user_id, TEST_DB)
        self.assertEqual(len(transactions), 0)

    def test_get_balance_summary(self):
        add_transaction(self.user_id, 'income', 'Salary', 2000.0, '', '2023-01-01', TEST_DB)
        add_transaction(self.user_id, 'expense', 'Rent', 800.0, '', '2023-01-02', TEST_DB)
        add_transaction(self.user_id, 'expense', 'Groceries', 200.0, '', '2023-01-03', TEST_DB)
        
        summary = get_balance_summary(self.user_id, TEST_DB)
        self.assertEqual(summary['total_income'], 2000.0)
        self.assertEqual(summary['total_expense'], 1000.0)
        self.assertEqual(summary['balance'], 1000.0)

    def test_get_category_expenses(self):
        add_transaction(self.user_id, 'expense', 'Food', 50.0, '', '2023-01-01', TEST_DB)
        add_transaction(self.user_id, 'expense', 'Food', 20.0, '', '2023-01-02', TEST_DB)
        add_transaction(self.user_id, 'expense', 'Transport', 30.0, '', '2023-01-03', TEST_DB)
        add_transaction(self.user_id, 'income', 'Salary', 1000.0, '', '2023-01-04', TEST_DB) # Should be ignored
        
        expenses = get_category_expenses(self.user_id, TEST_DB)
        self.assertEqual(len(expenses), 2)
        
        # 'Food' should be first because it has higher total (70.0 vs 30.0)
        self.assertEqual(expenses[0]['category'], 'Food')
        self.assertEqual(expenses[0]['total'], 70.0)
        self.assertEqual(expenses[1]['category'], 'Transport')
        self.assertEqual(expenses[1]['total'], 30.0)

if __name__ == '__main__':
    unittest.main()
