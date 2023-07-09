# This is the start of my coding for our accounting system in the office
from account_manager import main as account_management
from transaction import main as transaction_management


def main():
    while True:
        print("Options:")
        print("1. Account Management")
        print("2. Transaction Management")
        print("3. Exit")

        choice = input("Select an option (1-3): ")

        if choice == "1":
            account_management()
        elif choice == "2":
            transaction_management()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
