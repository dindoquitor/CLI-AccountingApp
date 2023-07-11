from new_transaction import transaction_management
from account import account_management
import clear_screen as c


def main_menu():
    while True:
        c.clear_screen()
        print("\n===== Main Menu =====\n")
        print("1. Add New Transaction")
        print("2. Add New Account")
        print("3. Exit")
        print("\n===== Main Menu =====\n")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            c.clear_screen()
            transaction_management()
        elif choice == "2":
            c.clear_screen()
            account_management()
        elif choice == "3":
            c.clear_screen()
            print("Goodbye...")
            break
        else:
            print("Invalid choice. Please enter a valid option (1-3).")


if __name__ == "__main__":
    main_menu()
