import sqlite3
import clear_screen as c
import os


def get_account_balances():
    try:
        conn = sqlite3.connect("transactions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT debit_account_code, credit_account_code, debit_amount, credit_amount FROM transactions")
        rows = cursor.fetchall()
        conn.close()

        account_balances = {}
        total_debit = 0
        total_credit = 0

        for row in rows:
            debit_account = row[0]
            credit_account = row[1]
            debit_amount = row[2]
            credit_amount = row[3]

            total_debit += debit_amount
            total_credit += credit_amount

            # Update account balances
            if debit_account in account_balances:
                account_balances[debit_account][0] += debit_amount
            else:
                account_balances[debit_account] = [debit_amount, 0]

            if credit_account in account_balances:
                account_balances[credit_account][1] += credit_amount
            else:
                account_balances[credit_account] = [0, credit_amount]

        return account_balances, total_debit, total_credit

    except sqlite3.OperationalError:
        print("Error: The database is not yet created. Please create the 'transactions.db' database.")
        return {}, 0, 0


account_balances, total_debit, total_credit = get_account_balances()


def get_account_name(account_code):
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT account_name FROM accounts WHERE account_code = ?", (account_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return "Unknown Account"


def generate_report():
    while True:
        # Print the header
        print("{:<50s}".format("TRIAL BALANCE\n"))
        print("{:<15s} {:<30s} {:<20s} {:<20s} {:<10s}".format(
            "\nAccount Code", "Account Name", "Debit Amount", "Credit Amount", "Balance\n"
        ))

        # Print the account balances
        total_balance = 0
        for account_code, (debit_amount, credit_amount) in account_balances.items():
            balance = debit_amount - credit_amount
            total_balance += balance
            print("{:<15s} {:<30s} {:<20.2f} {:<20.2f} {:<10.2f}".format(
                account_code, get_account_name(account_code), debit_amount, credit_amount, balance
            ))

        # Print the total debit and credit amounts
        print("{:<15s} {:<30s} {:<20.2f} {:<20.2f} {:<10.2f}".format(
            "Total:", "", total_debit, total_credit, total_balance
        ))

        # Prompt the user for input
        choice = input("\n\nType 'X' and Enter to exit: ")
        if choice.lower() == "x":
            print("Exiting...")
            break
        else:
            print()  # Print an empty line before generating another report


# def generate_file():
#     # Create an empty string to store the report content
#     report_content = ""
#
#     # Append the header to the report content
#     report_content += "{:<50s}\n".format("TRIAL BALANCE")
#     report_content += "{:<15s} {:<30s} {:<20s} {:<20s} {:<10s}\n".format(
#         "Account Code", "Account Name", "Debit Amount", "Credit Amount", "Balance"
#     )
#
#     # Append the account balances to the report content
#     total_balance = 0
#     for account_code, (debit_amount, credit_amount) in account_balances.items():
#         balance = debit_amount - credit_amount
#         total_balance += balance
#         report_content += "{:<15s} {:<30s} {:<20.2f} {:<20.2f} {:<10.2f}\n".format(
#             account_code, get_account_name(account_code), debit_amount, credit_amount, balance
#         )
#
#     # Append the total debit and credit amounts to the report content
#     report_content += "{:<15s} {:<30s} {:<20.2f} {:<20.2f} {:<10.2f}\n".format(
#         "Total:", "", total_debit, total_credit, total_balance
#     )
#
#     # Return the generated report content
#     return report_content

def generate_file():
    # Create an empty string to store the report content
    report_content = ""

    # Append the header to the report content
    report_content += "TRIAL BALANCE\n\n"
    headers = ["Account Code", "Account Name", "Debit Amount", "Credit Amount", "Balance"]
    table_data = []

    # Set the locale to the user's default locale
    locale.setlocale(locale.LC_ALL, "")

    # Append the account balances to the table data
    total_balance = 0
    for account_code, (debit_amount, credit_amount) in account_balances.items():
        balance = debit_amount - credit_amount
        total_balance += balance
        account_name = get_account_name(account_code)

        # Format amounts with commas and 2 decimal places
        debit_amount_formatted = locale.format_string("%.2f", debit_amount, grouping=True)
        credit_amount_formatted = locale.format_string("%.2f", credit_amount, grouping=True)
        balance_formatted = locale.format_string("%.2f", balance, grouping=True)

        table_data.append([account_code, account_name, debit_amount_formatted, credit_amount_formatted, balance_formatted])

    # Append the total debit and credit amounts to the table data
    total_debit_formatted = locale.format_string("%.2f", total_debit, grouping=True)
    total_credit_formatted = locale.format_string("%.2f", total_credit, grouping=True)
    total_balance_formatted = locale.format_string("%.2f", total_balance, grouping=True)

    table_data.append(["Total:", "", total_debit_formatted, total_credit_formatted, total_balance_formatted])

    # Generate the formatted table
    table = tabulate(table_data, headers, tablefmt="psql")

    # Append the formatted table to the report content
    report_content += table

    # Return the generated report content
    return report_content


def save_report_to_file(report_content, file_name):
    try:
        with open(file_name, "w") as file:
            file.write(report_content)
        print(f"Report saved successfully to '{file_name}'.")
    except IOError:
        print(f"Error: Failed to save report to '{file_name}'.")


# Example usage
def save_report():
    # Generate the report content
    report_content = generate_file()

    # Get the file name from the user
    file_name = input("Enter the file name: ")

    # Get the directory path from the user
    directory_path = input("Enter the directory path (leave empty for current directory): ")

    # If directory path is not provided, use the current directory
    if not directory_path:
        directory_path = os.getcwd()

    # Construct the full file path
    file_path = os.path.join(directory_path, file_name)

    # Save the report to the specified file path
    save_report_to_file(report_content, file_path)


def trial_balance():
    while True:
        c.clear_screen()
        print("\n===== Reports =====\n")
        print("1. Trial Balance")
        print("2. Save Report to txt file")
        print("3. Exit")
        print("\n===== Report =====\n")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            c.clear_screen()
            generate_report()
        elif choice == "2":
            c.clear_screen()
            save_report()
        elif choice == "3":
            c.clear_screen()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-2).")


if __name__ == "__main__":
    trial_balance()
