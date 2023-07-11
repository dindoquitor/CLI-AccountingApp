import sqlite3


def print_account_details(account_code, account_name, debit_amount, credit_amount, balance):
    """Prints the account details in a formatted table."""
    print("{:<15s} {:<30s} {:<20s} {:<20s} {:<10s}".format(
        "Account Code", "Account Name", "Debit Amount", "Credit Amount", "Balance"))
    print("{:<15s} {:<30s} {:<20d} {:<20d} {:<10d}".format(
        account_code, account_name, debit_amount, credit_amount, balance))


def get_account_balances():
    transaction_conn = sqlite3.connect("transactions.db")
    transaction_cursor = transaction_conn.cursor()
    transaction_cursor.execute(
        "SELECT debit_account_code, credit_account_code, debit_amount, credit_amount FROM transactions")
    transaction_rows = transaction_cursor.fetchall()
    transaction_conn.close()

    account_balances = {}

    account_conn = sqlite3.connect("accounts.db")
    account_cursor = account_conn.cursor()
    account_cursor.execute("SELECT account_code, account_name FROM accounts")
    account_rows = account_cursor.fetchall()
    account_conn.close()

    for row in transaction_rows:
        debit_account = row[0]
        credit_account = row[1]
        debit_amount = row[2]
        credit_amount = row[3]

        # Calculate net balance for debit account
        if debit_account in account_balances:
            account_balances[debit_account] += debit_amount
        else:
            account_balances[debit_account] = debit_amount

        # Calculate net balance for credit account
        if credit_account in account_balances:
            account_balances[credit_account] -= credit_amount
        else:
            account_balances[credit_account] = -credit_amount

    # Add account names to the account_balances dictionary
    for row in account_rows:
        account_code = row[0]
        account_name = row[1]
        if account_code in account_balances:
            account_balances[account_code] = (account_name, account_balances[account_code])

    return account_balances


# Example usage
account_balances = get_account_balances()
# for account, (account_name, balance) in account_balances.items():
#     print(account, account_name, balance)
#
#     account_balances = get_account_balances()

# Print the header row
print("{:<15s} {:<30s} {:<20s} {:<20s} {:<10s}".format(
    "Account Code", "Account Name", "Debit Amount", "Credit Amount", "Balance",
))
#
# Iterate over account balances and print each row
for account, (account_name, balance) in account_balances.items():
    debit_amount = balance if balance >= 0 else ""
    credit_amount = -balance if balance < 0 else ""
    balance = balance if balance != 0 else ""

    print("{:<15s} {:<30s} {:<20s} {:<20s} {:<10s}".format(
        account, account_name, str(debit_amount), str(credit_amount), str(balance)

    ))

# if __name__ == "__main__":
#   account_code = "123456789"
#   account_name = "My Account"
#   debit_amount = 100
#   credit_amount = 50
#   balance = debit_amount - credit_amount
#   print_account_details(account_code, account_name, debit_amount, credit_amount, balance)