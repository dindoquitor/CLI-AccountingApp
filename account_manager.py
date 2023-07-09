from account import Account, SubsidiaryLedger
from file_handler import read_accounts_from_file, write_account_to_file


def create_account(accounts):
    while True:
        name = input("Enter account name: ")
        code = input("Enter account code: ")

        if is_existing_account(accounts, name, code):
            print("Account already exists. Please try again.")
            continue

        if len(code) > 8:
            print("Account code cannot exceed 8 digits. Please try again.")
            continue

        account = Account(name, code)
        print("Account created successfully:")
        print(account)

        accounts[code] = account

        while True:
            choice = input("Do you want to add a subsidiary ledger? (yes/no): ")
            if choice.lower() == "yes":
                add_subsidiary_ledger(account)
            elif choice.lower() == "no":
                break
            else:
                print("Please answer with 'yes' or 'no'.")

        choice = input("Do you want to create another account? (yes/no): ")
        if choice.lower() != "yes":
            break


def add_subsidiary_ledger(account):
    name = input("Enter subsidiary ledger name: ")
    code = input("Enter subsidiary ledger code: ")

    if len(code) > 6:
        print("Subsidiary ledger code cannot exceed 6 digits.")
        return

    for ledger in account.subsidiary_ledgers:
        if ledger.code.lower() == code.lower():
            print("Subsidiary ledger code already exists.")
            return

    subsidiary_ledger = SubsidiaryLedger(name, code)
    print("Subsidiary ledger created successfully:")
    print(subsidiary_ledger)

    account.subsidiary_ledgers.append(subsidiary_ledger)


def edit_subsidiary_ledger(account):
    code = input("Enter subsidiary ledger code to edit: ")

    ledger_found = False
    for ledger in account.subsidiary_ledgers:
        if ledger.code.lower() == code.lower():
            new_name = input("Enter new subsidiary ledger name: ")
            new_code = input("Enter new subsidiary ledger code: ")
            if len(new_code) > 6:
                print("Subsidiary ledger code cannot exceed 6 digits.")
                return

            ledger.name = new_name
            ledger.code = new_code
            ledger_found = True
            print("Subsidiary ledger updated successfully.")
            break

    if not ledger_found:
        print("Subsidiary ledger not found.")


def edit_account(accounts):
    account_identifier = input("Enter the account code to edit: ")
    if account_identifier in accounts:
        account = accounts[account_identifier]

        new_name = input("Enter new account name: ")
        new_code = input("Enter new account code: ")
        if len(new_code) > 8:
            print("Account code cannot exceed 8 digits.")
            return

        account.name = new_name
        account.code = new_code
        print("Account updated successfully.")
    else:
        print("Account not found.")


def delete_account(accounts):
    account_identifier = input("Enter the account code to delete: ")
    if account_identifier in accounts:
        del accounts[account_identifier]
        print("Account deleted successfully.")
    else:
        print("Account not found.")


def delete_subsidiary_ledger(account):
    code = input("Enter subsidiary ledger code to delete: ")

    ledger_found = False
    for ledger in account.subsidiary_ledgers:
        if ledger.code.lower() == code.lower():
            account.subsidiary_ledgers.remove(ledger)
            ledger_found = True
            print("Subsidiary ledger deleted successfully.")
            break

    if not ledger_found:
        print("Subsidiary ledger not found.")


def is_existing_account(accounts, name, code):
    for account in accounts.values():
        if account.name.lower() == name.lower() or account.code.lower() == code.lower():
            return True
    return False


def main():
    accounts = read_accounts_from_file()

    while True:
        choice = input("What would you like to do? (1. Create account / 2. Edit account / 3. Delete account / 4. Add "
                       "subsidiary ledger / 5. Edit subsidiary ledger / 6. Delete subsidiary ledger / 7. Quit): ")
        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            edit_account(accounts)
        elif choice == "3":
            delete_account(accounts)
        elif choice == "4":
            account_identifier = input("Enter the account code to add subsidiary ledger: ")
            if account_identifier in accounts:
                add_subsidiary_ledger(accounts[account_identifier])
            else:
                print("Account not found.")
        elif choice == "5":
            account_identifier = input("Enter the account code to edit subsidiary ledger: ")
            if account_identifier in accounts:
                edit_subsidiary_ledger(accounts[account_identifier])
            else:
                print("Account not found.")
        elif choice == "6":
            account_identifier = input("Enter the account code to delete subsidiary ledger: ")
            if account_identifier in accounts:
                delete_subsidiary_ledger(accounts[account_identifier])
            else:
                print("Account not found.")
        elif choice == "7":
            write_account_to_file(accounts)
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
