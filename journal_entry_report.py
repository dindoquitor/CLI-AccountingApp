import sqlite3
from tabulate import tabulate
import clear_screen as c
import os
import locale


def get_journal_entries():
    try:
        conn = sqlite3.connect("transactions.db")
        cursor = conn.cursor()
        cursor.execute("SELECT debit_account_code, credit_account_code, description, debit_amount, credit_amount, "
                       "reference_date, reference_code FROM transactions")
        rows = cursor.fetchall()
        conn.close()

        journal_entries = []

        for row in rows:
            debit_account = row[0]
            credit_account = row[1]
            description = row[2]
            debit_amount = row[3]
            credit_amount = row[4]
            reference_date = row[5]
            reference_code = row[6]

            journal_entries.append((debit_account, credit_account, description, debit_amount, credit_amount,
                                    reference_date, reference_code))

        return journal_entries

    except sqlite3.OperationalError:
        print("Error: The database is not yet created. Please create the 'transactions.db' database.")
        return []


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


def generate_journal_entry_report():
    report_content = ""
    while True:
        # Print the header
        print("{:<50s}".format("JOURNAL ENTRY REPORT\n"))
        headers = ["Reference Code", "Account Code", "Account Name", "Debit Amount", "Credit Amount", "Date"]
        table_data = []

        # Set the locale to the user's default locale
        locale.setlocale(locale.LC_ALL, "")

        # Fetch the journal entries
        journal_entries = get_journal_entries()

        # Populate the table data
        for entry in journal_entries:
            debit_account = entry[0]
            credit_account = entry[1]
            description = entry[2]
            debit_amount = entry[3]
            credit_amount = entry[4]
            reference_date = entry[5]
            reference_code = entry[6]

            account_name_debit = get_account_name(debit_account)
            account_name_credit = get_account_name(credit_account)

            # Format amounts with commas and two decimal places
            debit_amount_formatted = locale.format_string("%.2f", debit_amount, grouping=True)
            credit_amount_formatted = locale.format_string("%.2f", credit_amount, grouping=True)

            table_data.append(
                [reference_code, debit_account, account_name_debit, debit_amount_formatted, "", reference_date])
            table_data.append(
                ["", credit_account, account_name_credit, "", credit_amount_formatted, ""])
            table_data.append(
                ["","", description, "", "", ""])
            table_data.append(" ")

        # Generate the formatted table
        table = tabulate(table_data, headers, tablefmt="psql",
                         colalign=("left", "left", "left", "right", "right", "center"),
                         maxcolwidths=[None, None, 150, None, None, None])

        # Print the table
        print(table)
        report_content += "JOURNAL ENTRIES\n"
        report_content += table

        return report_content


def print_journal_entry():
    while True:
        generate_journal_entry_report()

        # Prompt the user for input
        choice = input("\n\nType 'X' and Enter to exit: ")
        if choice.lower() == "x":
            print("Exiting...")
            break
        else:
            print()  # Print an empty line before generating another report


def save_journal_entry_report(report_content, file_name):
    try:
        with open(file_name, "w") as file:
            file.write(report_content)
            print(f"Journal entry report saved successfully to '{file_name}'.")
    except IOError:
        print(f"Error: Failed to save journal entry report to '{file_name}'.")


def generate_journal_entry_report_file():
    # Generate the journal entry report content
    report_content = generate_journal_entry_report()
    # Get the file name from the user
    file_name = input("Enter the file name: ")

    # Get the directory path from the user
    directory_path = input("Enter the directory path (leave empty for current directory): ")

    # If directory path is not provided, use the current directory
    if not directory_path:
        directory_path = os.getcwd()

    # Construct the full file path
    file_path = os.path.join(directory_path, file_name)

    # Save the journal entry report to the specified file path
    save_journal_entry_report(report_content, file_path)


def journal_entry_report():
    while True:
        c.clear_screen()
        print("\n===== Reports =====\n")
        print("1. Journal Entry Report")
        print("2. Save Journal Entry Report file")
        print("3. Exit")
        print("\n===== Report =====\n")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            c.clear_screen()
            print_journal_entry()
        elif choice == "2":
            c.clear_screen()
            generate_journal_entry_report_file()
        elif choice == "3":
            c.clear_screen()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-3).")


if __name__ == "__main__":
    journal_entry_report()
