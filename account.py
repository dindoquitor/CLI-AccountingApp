import sqlite3
import clear_screen as clean

class Account:
    def __init__(self, account_code, account_name, normal_balance):
        self.account_code = account_code
        self.account_name = account_name
        self.normal_balance = normal_balance

    def __str__(self):
        return f"Account Code: {self.account_code}\n" \
               f"Account Name: {self.account_name}\n" \
               f"Normal Balance: {self.normal_balance}\n"


def create_table():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                        account_code TEXT,
                        account_name TEXT,
                        normal_balance TEXT)''')
    conn.commit()
    conn.close()


def save_account(account):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO accounts (account_code, account_name, normal_balance)
        VALUES (?, ?, ?)
    ''', (account.account_code, account.account_name, account.normal_balance))
    conn.commit()
    conn.close()


def get_accounts():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    conn.close()

    accounts = []
    for row in rows:
        account_code, account_name, normal_balance = row
        account = Account(account_code, account_name, normal_balance)
        accounts.append(account)

    return accounts


def show_accounts(accounts):
    while True:
        print("Viewing Accounts in the database:")
        if not accounts:
            print("No accounts found.")
        else:
            for i, account in enumerate(accounts, start=1):
                print(f"{i}.")
                print(account)

        option = input("Press Enter to continue to next page or enter 'x' to exit the viewing : ")
        if option.lower() == 'x':
            break


def display_menu():
    print("\n===== Account Management Menu =====\n")
    print("1. Add Account")
    print("2. View Accounts")
    print("3. Edit Account")
    print("4. Delete Account")
    print("5. Exit")
    print("\n===== Account Management Menu =====\n")


def check_account_exists(account_code):
    """
    Check if an account with the given account code exists in the database.

    Args:
        account_code (str): The account code to check.

    Returns:
        bool: True if the account code exists, False otherwise.
    """
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_code = ?", (account_code,))
    rows = cursor.fetchall()
    conn.close()

    return bool(rows)


def add_account():
    while True:
        account_code = input("Enter the account code: ")
        if not account_code:
            print("Invalid account code. Account code is required. Please try again.")
            continue
        if check_account_exists(account_code):
            print("Invalid account code. Account code already exists. Please try again.")
            continue
        break

    while True:
        account_name = input("Enter the account name: ")
        if not account_name:
            print("Invalid account name. Account name is required. Please try again.")
            continue
        break

    while True:
        normal_balance = input("Enter the normal balance (debit/credit): ")
        if normal_balance.lower() not in ["debit", "credit"]:
            print("Invalid normal balance. Please enter 'debit' or 'credit'.")
            continue
        break

    account = Account(account_code, account_name, normal_balance)
    save_account(account)
    print("Account added successfully.")

    while True:
        save_option = input("Do you want to save more accounts? (y/n): \n")
        if save_option.lower() == "y":
            add_account()
        elif save_option.lower() == "n":
            break
        else:
            print("Invalid option. Please enter 'y' to add more accounts or 'n' to exit.\n")


def edit_account():
    while True:
        accounts = get_accounts()
        show_accounts(accounts)

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            account_index_str = input("\nEnter the index of the account to edit: ")

            if not account_index_str.isdigit():
                attempts += 1
                print("Invalid input. Please enter a valid number.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!")
                    return
                else:
                    continue

            account_index = int(account_index_str) - 1

            if 0 <= account_index < len(accounts):
                # Account index is valid, proceed with editing
                break
            else:
                attempts += 1
                print("Invalid account index. Please try again.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!.")
                    return

        if 0 <= account_index < len(accounts):
            account = accounts[account_index]
            print("Selected Account:")
            print(account)

            account_name = input("Enter the new account name (leave empty to keep current): ")
            if account_name:
                account.account_name = account_name

            account_code = input("Enter the new account code (leave empty to keep current): ")
            if account_code:
                if check_account_exists(account_code):
                    print("Invalid account code. Account code already exists.")
                else:
                    account.account_code = account_code

            normal_balance = input("Enter the new normal balance (debit/credit) "
                                   "(leave empty to keep current): ")
            if normal_balance.lower() in ["debit", "credit"]:
                account.normal_balance = normal_balance

            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute('''UPDATE accounts SET 
                              account_name = ?, 
                              account_code = ?, 
                              normal_balance = ? 
                              WHERE rowid = ?''',
                           (account.account_name, account.account_code, account.normal_balance,
                            account_index + 1))
            conn.commit()
            conn.close()

            print("Account edited successfully.")
        else:
            print("Invalid account index.")

        while True:
            more_option = input("Do you want to edit more accounts? (y/n): ")
            if more_option.lower() == "y":
                break
            elif more_option.lower() == "n":
                return
            else:
                print("Invalid option. Please enter 'y' to edit more accounts or 'n' to exit.")


def delete_account():
    while True:
        accounts = get_accounts()
        show_accounts(accounts)

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            account_index_str = input("\nEnter the index of the account to edit: ")

            if not account_index_str.isdigit():
                attempts += 1
                print("Invalid input. Please enter a valid number.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!.")
                    return
                else:
                    continue

            account_index = int(account_index_str) - 1

            if 0 <= account_index < len(accounts):
                # Account index is valid, proceed with editing
                break
            else:
                attempts += 1
                print("Invalid account index. Please try again.")

                if attempts == max_attempts:
                    print("Maximum number of attempts reached. Goodbye!.")
                    return

        if 0 <= account_index < len(accounts):
            account = accounts[account_index]
            print("Selected Account:")
            print(account)

            confirm = input("Are you sure you want to delete this account? (y/n): ")
            if confirm.lower() == "y":
                conn = sqlite3.connect("accounts.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM accounts WHERE rowid = ?", (account_index + 1,))
                conn.commit()
                conn.close()

                print("Account deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("Invalid account index.")

        while True:
            more_option = input("Do you want to delete more accounts? (y/n): ")
            if more_option.lower() == "y":
                break
            elif more_option.lower() == "n":
                return
            else:
                print("Invalid option. Please enter 'y' to delete more accounts or 'n' to exit.")


def account_management():
    create_table()

    while True:
        clean.clear_screen()
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            clean.clear_screen()
            add_account()
        elif choice == "2":
            clean.clear_screen()
            accounts = get_accounts()
            show_accounts(accounts)
        elif choice == "3":
            clean.clear_screen()
            edit_account()
        elif choice == "4":
            clean.clear_screen()
            delete_account()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            clean.clear_screen()
            print("Invalid choice. Please enter a valid option (1-5).")


if __name__ == "__main__":
    account_management()
