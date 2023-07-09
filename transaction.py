import json


class Transaction:
    transaction_count = 0

    def __init__(self, account_code, amount, description, transaction_type):
        Transaction.transaction_count += 1
        self.transaction_id = Transaction.transaction_count
        self.account_code = account_code
        self.amount = amount
        self.description = description
        self.transaction_type = transaction_type

    def __str__(self):
        return f"Transaction ID={self.transaction_id}, Account Code={self.account_code}, Amount={self.amount}, " \
               f"Description={self.description}, Type={self.transaction_type}"


def add_transaction(transactions):
    while True:
        description = input("Enter description: ")

        while True:
            transaction_type = input("Enter transaction type (debit/credit): ")
            if transaction_type.lower() in ["debit", "credit"]:
                break
            else:
                print("Invalid transaction type. Please enter 'debit' or 'credit'.")

        while True:
            account_code = input("Enter account code: ")
            if len(account_code) == 8:
                break
            else:
                print("Invalid account code. Please enter a 8-digit code.")

        while True:
            try:
                amount = float(input("Enter amount: "))
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")

        print("Transaction details:")
        print("Description:", description)
        print("Transaction type:", transaction_type)
        print("Account code:", account_code)
        print("Amount:", amount)

        # while True:
        #     choice = input("Do you want to save this transaction? (yes/no): ")
        #     if choice.lower() == "yes":
        #         transaction = Transaction(account_code, amount, description, transaction_type)
        #         transactions.append(transaction)
        #         print("Transaction saved successfully.")
        #         break
        #     elif choice.lower() == "no":
        #         print("Transaction not saved.")
        #         break
        #     else:
        #         print("Invalid choice. Please enter 'yes' or 'no'.")

        add_another = input("Do you want to add another transaction? (yes/no): ")
        if add_another.lower() != "yes":
            break
        else:
            continue


def edit_transaction(transactions):
    transaction_id = int(input("Enter the transaction ID to edit: "))

    for transaction in transactions:
        if transaction.transaction_id == transaction_id:
            print("Found transaction:")
            print(transaction)

            account_code = input("Enter new account code: ")
            amount = float(input("Enter new amount: "))

            while True:
                transaction_type = input("Enter new transaction type (debit/credit): ")
                if transaction_type.lower() in ["debit", "credit"]:
                    break
                else:
                    print("Invalid transaction type. Please enter 'debit' or 'credit'.")

            description = input("Enter new description: ")

            transaction.account_code = account_code
            transaction.amount = amount
            transaction.transaction_type = transaction_type
            transaction.description = description

            print("Transaction updated successfully:")
            print(transaction)
            break
    else:
        print("Transaction not found.")


def delete_transaction(transactions):
    transaction_id = int(input("Enter the transaction ID to delete: "))

    for transaction in transactions:
        if transaction.transaction_id == transaction_id:
            print("Found transaction to delete:")
            print(transaction)
            transactions.remove(transaction)
            print("Transaction deleted successfully.")
            break
    else:
        print("Transaction not found.")


def save_transactions_to_file(transactions):
    file_name = "transactions.txt"

    try:
        with open(file_name, "w") as file:
            json_transactions = [transaction.__dict__ for transaction in transactions]
            json.dump(json_transactions, file, indent=4)

        print("Transactions saved to file successfully.")
    except IOError:
        print("Error writing to the file.")


def check_balance(transactions):
    total_debit = 0
    total_credit = 0

    for transaction in transactions:
        if transaction.transaction_type.lower() == "debit":
            total_debit += transaction.amount
        elif transaction.transaction_type.lower() == "credit":
            total_credit += transaction.amount

    if total_debit == total_credit:
        print("Debit and credit amounts are balanced.")
    else:
        print("Debit and credit amounts are not balanced.")


def main():
    print("Transaction Management")
    transactions = []

    while True:
        print("Options:")
        print("1. Add Transaction")
        print("2. Edit Transaction")
        print("3. Delete Transaction")
        print("4. Save Transactions to File")
        print("5. Check Balance")
        print("6. Quit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            edit_transaction(transactions)
        elif choice == "3":
            delete_transaction(transactions)
        elif choice == "4":
            save_transactions_to_file(transactions)
        elif choice == "5":
            check_balance(transactions)
        elif choice == "6":
            exit_choice = input("Are you sure you want to exit? (yes/no): ")
            if exit_choice.lower() == "yes":
                print("Exiting the program.")
                break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
