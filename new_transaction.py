import sqlite3
import clear_screen as c
from invalid_attempts import InvalidAttemptChecker as attemptChecker
from datetime import datetime
import re
import sys


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_reference_code(reference_code):
    pattern = r"^(JEV3|JEV2|JEV4|JEV5|JEV6)-\d{2}-\d{2}-\d{4}$"
    return re.match(pattern, reference_code) is not None


class Transaction:
    def __init__(self, description, debit_amount, debit_account_code, credit_amount, credit_account_code,
                 reference_date, reference_code):
        self.description = description
        self.debit_amount = debit_amount
        self.debit_account_code = debit_account_code
        self.credit_amount = credit_amount
        self.credit_account_code = credit_account_code
        self.reference_date = reference_date
        self.reference_code = reference_code

    def __str__(self):
        return f"Description: {self.description}\n" \
               f"Debit Amount: {self.debit_amount}\n" \
               f"Debit Account Code: {self.debit_account_code}\n" \
               f"Credit Amount: {self.credit_amount}\n" \
               f"Credit Account Code: {self.credit_account_code}\n" \
               f"Reference Date: {self.reference_date}\n" \
               f"Reference Code: {self.reference_code}\n"


def create_table():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        description TEXT,
                        debit_amount REAL,
                        debit_account_code TEXT,
                        credit_amount REAL,
                        credit_account_code TEXT,
                        reference_date TEXT,
                        reference_code TEXT)''')
    conn.commit()
    conn.close()


def save_transaction(transaction):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (description, debit_amount, debit_account_code, credit_amount, 
                                 credit_account_code, reference_date, reference_code)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (transaction.description, transaction.debit_amount, transaction.debit_account_code,
          transaction.credit_amount, transaction.credit_account_code, transaction.reference_date,
          transaction.reference_code))
    conn.commit()
    conn.close()


def check_account_exists(account_code):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_code = ?", (account_code,))
    rows = cursor.fetchall()
    conn.close()

    if rows:
        return True
    return False


def add_new_transaction():
    invalid_checker = attemptChecker(max_attempts=3)
    print("\n====New Transaction Module====\n")

    while True:

        while True:
            if invalid_checker.is_max_attempts_exceeded():
                print("Exceeded maximum number of invalid attempts. Exiting...")
                return

            description = input("Enter the description: ")
            if not description:
                print("Invalid description. Description is required.")
                invalid_checker.increment_attempts()
            else:
                invalid_checker.reset_attempts()
                break

        debit_amount = None
        credit_amount = None

        while debit_amount is None or credit_amount is None:
            if invalid_checker.is_max_attempts_exceeded():
                print("Exceeded maximum number of invalid attempts. Exiting...")
                return

            debit_amount_str = input("Enter the debit amount: ")
            credit_amount_str = input("Enter the credit amount: ")

            try:
                debit_amount = float(debit_amount_str)
                credit_amount = float(credit_amount_str)
                invalid_checker.reset_attempts()
            except ValueError:
                print("Invalid amount. Please enter valid numbers for debit and credit amounts.")
                invalid_checker.increment_attempts()

        debit_account_code = None
        credit_account_code = None

        while not check_account_exists(debit_account_code) or not check_account_exists(credit_account_code):
            if invalid_checker.is_max_attempts_exceeded():
                print("Exceeded maximum number of invalid attempts. Exiting...")
                return

            debit_account_code = input("Enter the debit account code: ")
            credit_account_code = input("Enter the credit account code: ")

            if not check_account_exists(debit_account_code):
                print(f"Invalid debit account code '{debit_account_code}'. Account code does not exist.")

            if not check_account_exists(credit_account_code):
                print(f"Invalid credit account code '{credit_account_code}'. Account code does not exist.")

            invalid_checker.increment_attempts()

        reference_date = None
        attempts = 0

        while attempts < invalid_checker.max_attempts:
            reference_date = input("Enter the reference date: ")
            attempts = 0

            # Perform your validation checks here
            if reference_date and is_valid_date(reference_date):
                break

            print("Invalid reference date. Please enter a valid date.")
            attempts += 1

        if attempts == invalid_checker.max_attempts:
            print("Exceeded maximum number of invalid attempts. Exiting...")
            return

        reference_code = None

        while attempts < invalid_checker.max_attempts:
            reference_code = input("Enter the reference code: ")

            # Perform your validation checks here
            if is_valid_reference_code(reference_code):
                attempts = 0
                break

            print("Invalid reference code. Please enter a valid code.")
            attempts += 1

        if attempts == invalid_checker.max_attempts:
            print("Exceeded maximum number of invalid attempts. Exiting...")
            return

        while debit_amount != credit_amount:
            print("Debit and credit amounts are not balanced. Please make sure the amounts are equal.")
            debit_amount_str = input("Enter the corrected debit amount: ")
            credit_amount_str = input("Enter the corrected credit amount: ")

            try:
                debit_amount = float(debit_amount_str)
                credit_amount = float(credit_amount_str)
            except ValueError:
                print("Invalid amount. Please enter valid numbers for debit and credit amounts.")

        transaction = Transaction(description, debit_amount, debit_account_code, credit_amount,
                                  credit_account_code, reference_date, reference_code)
        save_transaction(transaction)
        print("Transaction saved successfully.")

        choice = input("Do you want to add another transaction? (y/n): ")
        if choice.lower() != "y":
            break


def get_saved_transactions():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    transactions = []
    for row in rows:
        description, debit_amount, debit_account_code, credit_amount, credit_account_code, \
            reference_date, reference_code = row
        transaction = Transaction(description, debit_amount, debit_account_code, credit_amount,
                                  credit_account_code, reference_date, reference_code)
        transactions.append(transaction)

    return transactions


def view_saved_transactions(transactions):
    while True:
        # transactions = get_saved_transactions()
        print("Lists of Saved Transactions:\n")
        if not transactions:
            print("No transactions found.\n")
        else:
            for t, transaction in enumerate(transactions, start=1):
                print(f"{t}")
                print(transaction)

        option = input("Type 'x' and press Enter to exit the viewing mode : ")
        if option.lower() == 'x':
            break


def edit_transaction():
    invalid_checker = attemptChecker(max_attempts=3)
    print("\n====Edit Transaction Module====\n")
    while True:
        transactions = get_saved_transactions()
        view_saved_transactions(transactions)

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            transaction_index_str = input("\nEnter the index of the transaction to edit: ")

            if not transaction_index_str.isdigit():
                attempts += 1
                print("Invalid input. Please enter a valid number.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!")
                    return
                else:
                    continue

            transaction_index = int(transaction_index_str) - 1

            if 0 <= transaction_index < len(transactions):
                # Transaction index is valid, proceed with editing
                break
            else:
                attempts += 1
                print("Invalid transaction index. Please try again.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!.")
                    return

        if 0 <= transaction_index < len(transactions):
            transaction = transactions[transaction_index]
            print("Selected Transaction:")
            print(transaction)

            # Prompt for updated values
            updated_transaction = Transaction(
                description=input(
                    f"Enter the new description (leave empty to keep current: {transaction.description}): ") or transaction.description,
                debit_amount=float(input(
                    f"Enter the new debit amount (leave empty to keep current: {transaction.debit_amount}): ") or transaction.debit_amount),
                debit_account_code=input(
                    f"Enter the new debit account code (leave empty to keep current: {transaction.debit_account_code}): ") or transaction.debit_account_code,
                credit_amount=float(input(
                    f"Enter the new credit amount (leave empty to keep current: {transaction.credit_amount}): ") or transaction.credit_amount),
                credit_account_code=input(
                    f"Enter the new credit account code (leave empty to keep current: {transaction.credit_account_code}): ") or transaction.credit_account_code,
                reference_date=input(
                    f"Enter the new reference date (leave empty to keep current: {transaction.reference_date}): ") or transaction.reference_date,
                reference_code=input(
                    f"Enter the new reference code (leave empty to keep current: {transaction.reference_code}): ") or transaction.reference_code,

            )
            
            while not check_account_exists(updated_transaction.debit_account_code) or not check_account_exists(updated_transaction.credit_account_code):
                if invalid_checker.is_max_attempts_exceeded():
                    print("Exceeded maximum number of invalid attempts. Exiting...")
                    return
                updated_transaction.debit_account_code = input("Enter the debit account code: ")
                updated_transaction.credit_account_code = input("Enter the credit account code: ")

                if not check_account_exists(updated_transaction.debit_account_code):
                    print(f"Invalid debit account code '{updated_transaction.debit_account_code}'. Account code does not exist.")

                if not check_account_exists(updated_transaction.credit_account_code):
                    print(f"Invalid credit account code '{updated_transaction.credit_account_code}'. Account code does not exist.")

                invalid_checker.increment_attempts()

            while updated_transaction.debit_amount != updated_transaction.credit_amount:
                print("Debit and credit amounts are not balanced. Please make sure the amounts are equal.")
                debit_amount_str = input("Enter the corrected debit amount: ")
                credit_amount_str = input("Enter the corrected credit amount: ")

                try:
                    updated_transaction.debit_amount = float(debit_amount_str)
                    updated_transaction.credit_amount = float(credit_amount_str)
                except ValueError:
                    print("Invalid amount. Please enter valid numbers for debit and credit amounts.")

            # Update the transaction in the database
            conn = sqlite3.connect("transactions.db")
            cursor = conn.cursor()
            cursor.execute('''UPDATE transactions SET 
                              description = ?, 
                              debit_amount = ?, 
                              debit_account_code = ?, 
                              credit_amount = ?, 
                              credit_account_code = ?, 
                              reference_date = ?, 
                              reference_code = ? 
                              WHERE rowid = ?''',
                           (updated_transaction.description, updated_transaction.debit_amount,
                            updated_transaction.debit_account_code,
                            updated_transaction.credit_amount, updated_transaction.credit_account_code,
                            updated_transaction.reference_date, updated_transaction.reference_code,
                            transaction_index + 1))
            conn.commit()
            conn.close()

            print("Transaction edited successfully.")
        else:
            print("Invalid transaction index.")

        while True:
            more_option = input("Do you want to edit more transactions? (y/n): ")
            if more_option.lower() == "y":
                break
            elif more_option.lower() == "n":
                return
            else:
                print("Invalid option. Please enter 'y' to edit more transactions or 'n' to exit.")


def delete_transaction():
    print("\n====Delete Transaction Module====\n")
    while True:
        transactions = get_saved_transactions()
        view_saved_transactions(transactions)

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            transaction_index_str = input("\nEnter the index of the transaction to delete: ")

            if not transaction_index_str.isdigit():
                attempts += 1
                print("Invalid input. Please enter a valid number.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!")
                    return
                else:
                    continue

            transaction_index = int(transaction_index_str) - 1

            if 0 <= transaction_index < len(transactions):
                # Transaction index is valid, proceed with deletion
                break
            else:
                attempts += 1
                print("Invalid transaction index. Please try again.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!")
                    return

        if 0 <= transaction_index < len(transactions):
            transaction = transactions[transaction_index]
            print("Selected Transaction:")
            print(transaction)

            confirm = input("Are you sure you want to delete this transaction? (y/n): ")
            if confirm.lower() == "y":
                conn = sqlite3.connect("transactions.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE rowid = ?", (transaction_index + 1,))
                conn.commit()
                conn.close()

                print("Transaction deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid transaction index.")

        while True:
            more_option = input("Do you want to delete more transactions? (y/n): ")
            if more_option.lower() == "y":
                break
            elif more_option.lower() == "n":
                return
            else:
                print("Invalid option. Please enter 'y' to delete more transactions or 'n' to exit.")


def transaction_management():
    create_table()
    while True:
        c.clear_screen()
        print("\n===== Transaction Management Menu =====\n")
        print("1. Add New Transaction")
        print("2. View Saved Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Exit")
        print("\n===== Transaction Management Menu =====\n")

        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            c.clear_screen()
            add_new_transaction()
        elif choice == "2":
            c.clear_screen()
            transactions = get_saved_transactions()
            view_saved_transactions(transactions)
        elif choice == "3":
            c.clear_screen()
            edit_transaction()
        elif choice == "4":
            c.clear_screen()
            delete_transaction()
        elif choice == "5":
            c.clear_screen()
            print("Goodbye!...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-5).")


if __name__ == "__main__":
    transaction_management()
