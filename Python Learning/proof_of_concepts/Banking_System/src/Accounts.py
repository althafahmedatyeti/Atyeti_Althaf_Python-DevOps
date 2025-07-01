class Bank_account:
    def __init__(self, account_id, name, balance, password):
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.password = password

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    def get_balance(self):
        return self.balance

    def display_all(self):
        print(f"Name: {self.name}")
        print(f"ID: {self.account_id}")
        print(f"Balance: ₹{self.balance}")

    def __repr__(self):
        return f"BankAccount(account_id='{self.account_id}', name='{self.name}', balance={self.balance})"
