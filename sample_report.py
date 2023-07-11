import sqlite3

def get_account_balances():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT debit_account_code, credit_account_code, debit_amount, credit_amount FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    account_balances = {}
    for row in rows:
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

    return account_balances

# Example usage
account_balances = get_account_balances()
for account, balance in account_balances.items():
    print("Account:", account, "Balance:", balance )

