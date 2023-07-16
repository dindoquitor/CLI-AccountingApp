import clear_screen as c
from account import account_management
from new_transaction import transaction_management
from trial_balance import trial_balance

import curses

def set_terminal_size(height, width):
    try:
        # Initialize the curses screen
        stdscr = curses.initscr()

        # Set the terminal size
        curses.resizeterm(height, width)

    finally:
        # End the curses screen
        curses.endwin()



def main_menu():
    set_terminal_size(25, 80)
    while True:
        c.clear_screen()
        print("\n===== Main Menu =====\n")
        print("1. Add New Transaction")
        print("2. Add New Account")
        print("3. Generate Report")
        print("4. Exit")
        print("\n===== Main Menu =====\n")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            c.clear_screen()
            set_terminal_size(25, 40)
            transaction_management()
        elif choice == "2":
            c.clear_screen()
            account_management()
        elif choice == "3":
            c.clear_screen()
            trial_balance()
        elif choice == "4":
            c.clear_screen()
            print("Goodbye...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-3).")


if __name__ == "__main__":
    main_menu()
