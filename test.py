def edit_transaction():
    while True:
        transactions = get_saved_transactions()
        show_transactions(transactions)

        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            transaction_index_str = input(
                "\nEnter the index of the transaction to edit: ")

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

            # TODO: Implement transaction editing logic here

        while True:
            more_option = input(
                "Do you want to edit more transactions? (y/n): ")
            if more_option.lower() == "y":
                break
            elif more_option.lower() == "n":
                return
            else:
                print(
                    "Invalid option. Please enter 'y' to edit more transactions or 'n' to exit.")
