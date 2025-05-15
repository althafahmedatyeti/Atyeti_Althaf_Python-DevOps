import logging
from src.Accounts import Bank_account
class MyAccount:
    logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s- %(levelname)s-%(message)s',
    filemode='w',
    encoding='utf-8'

)
    def __init__(self):
        self.account={}
    def create_account(self,name,account_id,balance,passs):

        if account_id in self.account:
            print("account already exists")
        else:
            account1=Bank_account(account_id,name,balance,passs)
            self.account[account_id]=account1
            print("Account created sucessful")
    def display_all_account(self):
        if not self.account:
            print("No Accounts are there")
        else:
            for i,j in self.account.items():
                j.display_all()
                print("-" * 20)
        logging.info("Displaying all accounts")
    def create_Account_flow(self):
        name = input("Enter your name")
        id = input("Enter id")
        balance = int(input("Deposit amount"))
        passs = input("Enter password")
        # self.account[id]=[name,balance,name]
        self.create_account(name, id, balance, passs)
        logging.info(f"Account created successfully : ID={id},name={name}")
    def Deposit_Account_flow(self):
        id = input("Enter id to Deposit: ")
        amount= int(input("Enter amount:"))
        if id in self.account:
            self.account[id].deposit(amount)
            logging.info(f"Deposited ₹{amount} to account ID={id}. New balance: ₹{self.account[id].balance}")

    def withdraw_flow(self):
        id = input("Enter your id ")
        amount = int(input("Enter amount To withdraw :"))
        current_balance = self.account[id].get_balance()
        if current_balance >= amount:
            self.account[id].withdraw(amount)
            logging.info(f"Withdrew ₹{amount} from account ID={id}. New balance: ₹{self.account[id].balance}")

        else:
            print("Unsffient Amount")
            logging.warning( f"Withdrawal of ₹{amount} failed for ID={id} — insufficient funds (balance: ₹{self.account[id].balance})")

    def check_balance_flow(self):
         eid = input("Enter your id")
         if eid in self.account:
             print(self.account[eid].get_balance())
         else:
             print("no account found")
         logging.info(f"Balance checked for ID={eid}")



obj=MyAccount()



