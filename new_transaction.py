import sqlite3
import clear_screen as c
from invalid_attempts import InvalidAttemptChecker as attemptChecker


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
        INSERT INTO transactions (description, debit_amount, debit_account_code, credit_amount, credit_account_code,
                                 reference_date, reference_code)
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
            debit_amount_str = input("Enter the debit amount: ")
            credit_amount_str = input("Enter the credit amount: ")

            try:
                debit_amount = float(debit_amount_str)
                credit_amount = float(credit_amount_str)
            except ValueError:
                print("Invalid amount. Please enter valid numbers for debit and credit amounts.")

        debit_account_code = input("Enter the debit account code: ")
        credit_account_code = input("Enter the credit account code: ")

        while not check_account_exists(debit_account_code):
            print(f"Invalid debit account code '{debit_account_code}'. Account code does not exist.")
            debit_account_code = input("Enter the correct debit account code: ")

        while not check_account_exists(credit_account_code):
            print(f"Invalid credit account code '{credit_account_code}'. Account code does not exist.")
            credit_account_code = input("Enter the correct credit account code: ")

        reference_date = input("Enter the reference date: ")
        reference_code = input("Enter the reference code: ")

        while debit_amount != credit_amount:
            print("Debit and credit amounts are not balanced. Please make sure the amounts are equal.")
            debit_amount_str = input("Enter the corrected debit amount: ")
            credit_amount_str = input("Enter the corrected credit amount: ")

            try:
                debit_amount = float(debit_amount_str)
                credit_amount = float(credit_amount_str)
            except ValueError:
                print("Invalid amount. Please enter valid numbers for debit and credit amounts.")

        transaction = Transaction(description, debit_amount, debit_account_code, credit_amount, credit_account_code,
                                  reference_date, reference_code)
        save_transaction(transaction)
        print("Transaction saved successfully.")

        choice = input("Do you want to add another transaction? (y/n): ")
        if choice.lower() != "y":
            break


def main_menu():
    while True:
        print("\n===== Transaction Management Menu =====")
        print("1. Add New Transaction")
        print("2. Exit")

        choice = input("Enter your choice (1-2): ")
        if choice == "1":
            c.clear_screen()
            add_new_transaction()
        elif choice == "2":
            c.clear_screen()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-2).")


if __name__ == "__main__":
    create_table()
    main_menu()
