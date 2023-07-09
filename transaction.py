class Transaction:
    def __init__(self, account_code, amount, description):
        self.account_code = account_code
        self.amount = amount
        self.description = description

    def __str__(self):
        return f"Transaction: Account Code={self.account_code}, Amount={self.amount}, Description={self.description}"


def add_transaction(transactions):
    account_code = input("Enter account code: ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    transaction = Transaction(account_code, amount, description)
    print("Transaction added successfully:")
    print(transaction)

    transactions.append(transaction)


def save_transactions_to_file(transactions):
    file_name = input("Enter the name of the text file to save transactions: ")
    try:
        with open(file_name, "w") as file:
            for transaction in transactions:
                file.write(str(transaction) + "\n")
        print("Transactions saved to file successfully.")
    except IOError:
        print("Error writing to the file.")


def main():
    print("Transaction Module")
    transactions = []

    while True:
        choice = input("What would you like to do? (1. Add Transaction / 2. Save Transactions to File / 3. Quit): ")
        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            save_transactions_to_file(transactions)
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
