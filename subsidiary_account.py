import sqlite3
import clear_screen as c
import account as gl
from invalid_attempts import InvalidAttemptChecker as ia


class SubsidiaryAccount:
    def __init__(self, subsidiary_account_code, account_name, normal_balance, account_code):
        self.subsidiary_account_code = subsidiary_account_code
        self.account_name = account_name
        self.normal_balance = normal_balance
        self.account_code = account_code

    def __str__(self):
        return f"Subsidiary Account Code: {self.subsidiary_account_code}\n" \
               f"Account Name: {self.account_name}\n" \
               f"Normal Balance: {self.normal_balance}\n" \
               f"Account Code: {self.account_code}"


def create_table():
    conn = sqlite3.connect("subsidiary_accounts.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS subsidiary_accounts (
                        subsidiary_account_code TEXT PRIMARY KEY,
                        account_name TEXT,
                        normal_balance TEXT,
                        account_code TEXT,
                        FOREIGN KEY (account_code) REFERENCES accounts(account_code))''')
    conn.commit()
    conn.close()


def save_subaccount(subaccount):
    conn = sqlite3.connect("subsidiary_accounts.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subsidiary_accounts (subsidiary_account_code, account_name, normal_balance, account_code) "
        "VALUES (?, ?, ?, ?)",
        (subaccount.subsidiary_account_code, subaccount.account_name, subaccount.normal_balance,
         subaccount.account_code))
    conn.commit()
    conn.close()


def get_subaccount():
    conn = sqlite3.connect("subsidiary_accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subsidiary_accounts")
    rows = cursor.fetchall()
    conn.close()

    subaccounts = []
    for row in rows:
        subsidiary_account_code, account_name, normal_balance, account_code = row
        subaccount = SubsidiaryAccount(subsidiary_account_code, account_name, normal_balance, account_code)
        subaccounts.append(subaccount)

    return subaccounts

    # cursor.execute("SELECT * FROM subsidiary_accounts WHERE subsidiary_account_code = ?",
    #                (subsidiary_account_code,))
    # row = cursor.fetchone()
    # conn.close()
    #
    # if row:
    #     subsidiary_account_code, account_name, normal_balance, account_code = row
    #     return SubsidiaryAccount(subsidiary_account_code, account_name, normal_balance, account_code)
    # else:
    #     return None


def delete_subaccount(subsidiary_account_code):
    conn = sqlite3.connect("subsidiary_accounts.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subsidiary_accounts WHERE subsidiary_account_code = ?",
                   (subsidiary_account_code,))
    conn.commit()
    conn.close()


def show_subaccounts(subaccounts):
    while True:
        print("\nViewing Subsidiary Accounts in the database:\n")
        if not subaccounts:
            print("No subsidiary accounts found.")
        else:
            for i, subaccount in enumerate(subaccounts, start=1):
                print(f"{i}.")
                print(subaccount)

        option = input("\nType 'x' and press Enter to exit the viewing mode : ")
        if option.lower() == 'x':
            break
    # conn = sqlite3.connect("subsidiary_accounts.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM subsidiary_accounts")
    # rows = cursor.fetchall()
    # conn.close()
    #
    # print("Subsidiary Accounts:")
    # if not rows:
    #     print("No subsidiary accounts found.")
    # else:
    #     for row in rows:
    #         subsidiary_account_code, account_name, normal_balance, account_code = row
    #         subaccount = SubsidiaryAccount(subsidiary_account_code, account_name, normal_balance, account_code)
    #         print(subaccount)


def check_sub_exists(subsidiary_account_code):
    """
    Check if an account with the given account code exists in the database.

    Args:
        account_code (str): The account code to check.

    Returns:
        bool: True if the account code exists, False otherwise.
        :param subsidiary_account_code:
    """
    conn = sqlite3.connect("subsidiary_accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subsidiary_accounts WHERE subsidiary_account_code = ?", (subsidiary_account_code,))
    rows = cursor.fetchall()
    conn.close()

    return bool(rows)


def add_subaccount():
    invalid_checker = ia(max_attempts=3)
    print("====Add Subsidiary Account Module====\n")

    while True:

        while True:
            if invalid_checker.is_max_attempts_exceeded():
                print("Maximum number of attempts reached. Goodbye!")
                return

            subsidiary_account_code = input("Enter the subsidiary account code: ")

            if not subsidiary_account_code:
                print("Invalid subsidiary account code. Please try again.")
                invalid_checker.increment_attempts()
                continue
            else:
                invalid_checker.reset_attempts()

            if check_sub_exists(subsidiary_account_code):
                print("Subsidiary account code already exists. Please try again.")
                invalid_checker.increment_attempts()
                continue
            else:
                invalid_checker.reset_attempts()
            break

        while True:
            if invalid_checker.is_max_attempts_exceeded():
                print("Maximum number of attempts reached. Goodbye!")
                return

            account_name = input("Enter the account name: ")

            if not account_name:
                print("Invalid account name. Please try again.")
                invalid_checker.increment_attempts()
                continue
            else:
                invalid_checker.reset_attempts()
                break

        while True:
            if invalid_checker.is_max_attempts_exceeded():
                print("Maximum number of attempts reached. Goodbye!")
                return

            normal_balance = input("Enter the normal balance (debit/credit: ")

            if not normal_balance:
                print("Invalid normal balance. Please try again.")
                invalid_checker.increment_attempts()
                continue
            else:
                invalid_checker.reset_attempts()
                break

        while True:
            if invalid_checker.is_max_attempts_exceeded():
                print("Maximum number of attempts reached. Goodbye!")
                return

            account_code = input("Enter the GL account code: ")

            if not account_code:
                print("Invalid GL account code. Please try again.")
                invalid_checker.increment_attempts()
                continue
            else:
                invalid_checker.reset_attempts()

            if not gl.check_account_exists(account_code):
                print("GL account code doesn't exists. Please try again.")
                invalid_checker.increment_attempts()
                continue
            else:
                invalid_checker.reset_attempts()
            break

        subaccount = SubsidiaryAccount(subsidiary_account_code, account_name, normal_balance, account_code)

        while True:
            save_option = input("Do you want to save the account? (y/n): \n")
            if save_option.lower() == "y":
                c.clear_screen()
                print(subaccount)
                save_subaccount(subaccount)
                new_acct = input("Do you want to add moRE accounts? (y/n): \n")
                if new_acct.lower() == "y":
                    add_subaccount()
                else:
                    return
            elif save_option.lower() == "n":
                print("Account not saved.")
                return
            else:
                print("Invalid option. Please enter 'y' to add more accounts or 'n' to exit.\n")


def edit_subaccount():
    global subsidiary_account_index
    invalid_checker = ia(max_attempts=3)

    while True:
        subaccounts = get_subaccount()
        show_subaccounts(subaccounts)

        while True:
            if invalid_checker.is_max_attempts_exceeded():
                print("Maximum number of attempts reached. Goodbye!")
                return

            subsidiary_account_index_str = input("Enter the index of the account code to edit: ")

            if not subsidiary_account_index_str.isdigit():
                print("Invalid input. Please enter a valid number.")
                invalid_checker.increment_attempts()
                continue

            subsidiary_account_index = int(subsidiary_account_index_str) - 1

            if 0 <= subsidiary_account_index < len(subaccounts):
                break
            else:
                print("Invalid input. Please enter a valid number.")
                invalid_checker.increment_attempts()
                continue

        if 0 <= subsidiary_account_index < len(subaccounts):
            subaccount = subaccounts[subsidiary_account_index]
            print(subaccount)

            updated_subaccount = SubsidiaryAccount(
                subsidiary_account_code=input(f"Enter the new subsidiary account code"
                                              f"(Leave empty to keep current: {subaccount.subsidiary_account_code}): "
                                              f"") or subaccount.subsidiary_account_code,
                account_name=input(
                    f"Enter the new account name (Leave empty to keep current: {subaccount.account_name}): "
                    f"") or subaccount.account_name,
                normal_balance=input(
                    f"Enter the new normal balance (Leave empty to keep current: {subaccount.normal_balance}): "
                    f"") or subaccount.normal_balance,
                account_code=input(
                    f"Enter the new GL account code (Leave empty to keep current: {subaccount.account_code}): "
                    f"") or subaccount.account_code
            )

            conn = sqlite3.connect("subsidiary_accounts.db")
            cursor = conn.cursor()
            cursor.execute('''UPDATE subsidiary_accounts SET
                           subsidiary_account_code = ?,
                           account_name = ?,
                           normal_balance = ?,
                           account_code = ?
                            WHERE rowid = ?''',
                           (updated_subaccount.subsidiary_account_code, updated_subaccount.account_name,
                            updated_subaccount.normal_balance, updated_subaccount.account_code,
                            subsidiary_account_index + 1))
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


def delete_subaccount():
    while True:
        subsidiary_account_code = input("Enter the subsidiary account code to delete: ")

        subaccount = get_subaccount()
        if subaccount:
            print("Selected Subsidiary Account:")
            print(subaccount)

            confirm = input("Are you sure you want to delete this subsidiary account? (y/n): ")
            if confirm.lower() == "y":
                delete_subaccount(subsidiary_account_code)
                print("Subsidiary account deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("Subsidiary account not found.")

        choice = input("Delete another subsidiary account? (y/n): ")
        if choice.lower() != "y":
            break


def subsidiary_account():
    create_table()
    while True:
        c.clear_screen()
        print("\n=== Subsidiary Account Menu ===")
        print("1. Add Subsidiary Account")
        print("2. Edit Subsidiary Account")
        print("3. Delete Subsidiary Account")
        print("4. Show Subsidiary Accounts")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            c.clear_screen()
            add_subaccount()
        elif choice == "2":
            c.clear_screen()
            edit_subaccount()
        elif choice == "3":
            c.clear_screen()
            delete_subaccount()
        elif choice == "4":
            c.clear_screen()
            subaccount = get_subaccount()
            show_subaccounts(subaccount)
        elif choice == "5":
            c.clear_screen()
            print("Exiting Subsidiary Account Menu...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-5).")


# Example usage
if __name__ == "__main__":
    subsidiary_account()
