import sqlite3
from tabulate import tabulate
import clear_screen as c
import os
import locale
from journal_entry_report import journal_entry_report
from invalid_attempts import InvalidAttemptChecker as attemptChecker
import pandas as pd


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
    report_content = ""
    while True:
        # Print the header
        # print("{:<50s}".format("TRIAL BALANCE\n"))
        

        headers = ["Account Code", "Account Name", "Debit Amount", "Credit Amount", "Balance"]
        table_data = []

        # Set the locale to the user's default locale
        locale.setlocale(locale.LC_ALL, "")

        # Populate the table data
        total_balance = 0
        for account_code, (debit_amount, credit_amount) in account_balances.items():
            balance = debit_amount - credit_amount
            total_balance += balance
            account_name = get_account_name(account_code)

            # Format amounts with commas and two decimal places
            debit_amount_formatted = locale.format_string("%.2f", debit_amount, grouping=True)
            credit_amount_formatted = locale.format_string("%.2f", credit_amount, grouping=True)
            balance_formatted = locale.format_string("%.2f", balance, grouping=True)

            table_data.append(
                [account_code, account_name, debit_amount_formatted, credit_amount_formatted, balance_formatted])

        
        # Append the total debit and credit amounts to the table data
        total_debit_formatted = locale.format_string("%.2f", total_debit, grouping=True)
        total_credit_formatted = locale.format_string("%.2f", total_credit, grouping=True)
        total_balance_formatted = locale.format_string("%.2f", total_balance, grouping=True)

        table_data.append(["Total:", "", total_debit_formatted, total_credit_formatted, total_balance_formatted])

        # Generate the formatted table
        table = tabulate(table_data, headers, tablefmt="psql", floatfmt=".2f",
                         colalign=("left", "left", "right", "right", "right"))

        # Print the table
        office = input("Name of Office: ").upper()
        report_date = input("Report Date: ").upper()
        c.clear_screen()
        report_content += f"{office}\nTRIAL BALANCE\n{report_date}\n\n{table}\n\033[92mCreated by: Dindo O. Quitor, CPA\033[0m\n"
        print(report_content)
        
        return report_content
        



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

def print_tb():
    attempts = attemptChecker(max_attempts=3)
    generate_report()
    while True:
        # Prompt the user for input
        if attempts.is_max_attempts_exceeded():
                print("Exceeded maximum number of invalid attempts. Exiting...")
                return
        choice = input("Type 'X' and Enter to exit: ")
        if choice.lower() == "x":
            print("Exiting...")
            attempts.reset_attempts()
            break
        else:
            print()  # Print an empty line before generating another report
            attempts.increment_attempts()
        

# def generate_file():
    # province = input("Type the name of your office?: ")
    # date_of_report = input("Type the date of report: ")
    # # Create an empty string to store the report content
    # report_content = ""

    # # Append the header to the report content
    # report_content += province + "\n"
    # report_content += "TRIAL BALANCE\n"
    # report_content += date_of_report + "\n"

    # headers = ["Account Code", "Account Name", "Debit Amount", "Credit Amount", "Balance"]
    # table_data = []

    # # Set the locale to the user's default locale
    # locale.setlocale(locale.LC_ALL, "")

    # # Append the account balances to the table data
    # total_balance = 0
    # for account_code, (debit_amount, credit_amount) in account_balances.items():
    #     balance = debit_amount - credit_amount
    #     total_balance += balance
    #     account_name = get_account_name(account_code)

    #     # Format amounts with commas and 2 decimal places
    #     debit_amount_formatted = locale.format_string("%.2f", debit_amount, grouping=True)
    #     credit_amount_formatted = locale.format_string("%.2f", credit_amount, grouping=True)
    #     balance_formatted = locale.format_string("%.2f", balance, grouping=True)

    #     table_data.append(
    #         [account_code, account_name, debit_amount_formatted, credit_amount_formatted, balance_formatted])

    # # Append the total debit and credit amounts to the table data
    # total_debit_formatted = locale.format_string("%.2f", total_debit, grouping=True)
    # total_credit_formatted = locale.format_string("%.2f", total_credit, grouping=True)
    # total_balance_formatted = locale.format_string("%.2f", total_balance, grouping=True)

    # table_data.append(["Total:", "", total_debit_formatted, total_credit_formatted, total_balance_formatted])

    # # Generate the formatted table
    # table = tabulate(table_data, headers, tablefmt="psql", floatfmt=".2f",
    #                  colalign=("left", "left", "right", "right", "right"))

    # # Append the formatted table to the report content
    # report_content += table

    # # Return the generated report content
    # return report_content


def save_report_to_file(report_content, file_name):
    attempts = attemptChecker(max_attempts=3)
    while True:
        try:
            with open(file_name, "w") as file:
                file.write(report_content)
            print(f"Report saved successfully to '{file_name}'.\n")
        except IOError:
            print(f"Error: Failed to save report to '{file_name}'.")
            
        if attempts.is_max_attempts_exceeded():
                print("Exceeded maximum number of invalid attempts. Exiting...")
                return
        # Prompt the user for input
        choice = input("Type 'X' and Enter to exit: ")
        if choice.lower() == "x":
            print("Exiting...")
            attempts.reset_attempts()
            break
        else:
            print()  # Print an empty line before generating another report
            attempts.increment_attempts()



# Example usage
def save_report():
   
    # Generate the report content
    report_content = generate_report()

    # Get the file name from the user
    file_name = input("Enter the file name: ")
    if file_name == "":
        file_name = "TRIAL BALANCE.TXT"
    else:
        file_name += ".txt"

    # Get the directory path from the user
    directory_path = input("Enter the directory path (leave empty for current directory): ")

    # If directory path is not provided, use the current directory
    if not directory_path:
        directory_path = os.getcwd()

    # Construct the full file path
    file_path = os.path.join(directory_path, file_name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"\033[91mDeleted existing file:\033[0m {file_path}")
    else:
        print(f"\033[92mNo existing file found:\033[0m {file_path}")

    # Save the report to the specified file path
    save_report_to_file(report_content, file_path)
    


def trial_balance():
    while True:
        c.clear_screen()
        print("\n===== Reports =====\n")
        print("1. Trial Balance")
        print("2. Journal Entries")
        print("3. Save TB to Text File")
        print("4. Save TB to Excel File")
        print("5. Exit")
        print("\n===== Report =====\n")

        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            c.clear_screen()
            print_tb()
        elif choice == "2":
            c.clear_screen()
            journal_entry_report()
        elif choice == "3":
            c.clear_screen()
            save_report()
        elif choice == "4":
            c.clear_screen()
            save_report_to_excel()
        elif choice == "5":
            c.clear_screen()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-4).")


if __name__ == "__main__":
    trial_balance()
