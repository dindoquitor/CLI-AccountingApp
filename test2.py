def add_new_transaction():
    invalid_checker = attemptChecker(max_attempts=3)
    index = 0

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

        index += 10
        transaction = Transaction(index, description, debit_amount, debit_account_code, credit_amount,
                                  credit_account_code, reference_date, reference_code)
        save_transaction(transaction)
        print("Transaction saved successfully.")

        choice = input("Do you want to add another transaction? (y/n): ")
        if choice.lower() != "y":
            break