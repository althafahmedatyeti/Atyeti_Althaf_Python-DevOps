# main.py

from src.transactions import MyAccount
from src.Accounts import Bank_account

def main():
    app=MyAccount()
    while True:
        print("\n--- ABC Bank Menu ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Display All Accounts")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            app.create_Account_flow()
        elif choice == '2':
            app.Deposit_Account_flow()
        elif choice == '3':
            app.withdraw_flow()
        elif choice == '4':
            app.check_balance_flow()
        elif choice == '5':
            app.display_all_account()
        elif choice == '6':
            print("Thank you for using ABC Bank.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
#Need TO add Extra Features......................