import abc
from collections import deque
import pandas as pd

# Queue
transaction_queue = deque()

# -----------------------------
# Admin Credentials
# -----------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# -----------------------------
# Abstract Class
# -----------------------------
class BankAccount(abc.ABC):

    def __init__(self, account_no, holder_name, balance=0):
        self.account_no = account_no
        self.holder_name = holder_name
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            transaction_queue.append(f"Deposit Rs.{amount} in {self.account_no}")
            print(f"Rs.{amount} deposited successfully.")
        else:
            print("Invalid Amount!")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.__balance:
            self.__balance -= amount
            transaction_queue.append(f"Withdraw Rs.{amount} from {self.account_no}")
            print(f"Rs.{amount} withdrawn successfully.")
        else:
            print("Insufficient Balance or Invalid Amount!")

    @abc.abstractmethod
    def display(self):
        pass


# -----------------------------
# Child Class
# -----------------------------
class SavingsAccount(BankAccount):

    def __init__(self, account_no, holder_name, balance=0):
        super().__init__(account_no, holder_name, balance)

    def display(self):
        print("\n------ Savings Account ------")
        print("Account No :", self.account_no)
        print("Holder Name:", self.holder_name)
        print("Balance    : Rs.", self.get_balance())


# -----------------------------
# Linked List Node
# -----------------------------
class Node:

    def __init__(self, account):
        self.account = account
        self.next = None


# -----------------------------
# Linked List
# -----------------------------
class LinkedList:

    def __init__(self):
        self.head = None

    def add(self, account):

        new_node = Node(account)

        if self.head is None:
            self.head = new_node

        else:
            temp = self.head

            while temp.next:
                temp = temp.next

            temp.next = new_node

    def __iter__(self):

        current = self.head

        while current:
            yield current.account
            current = current.next


# -----------------------------
# Bank Class (Iterator)
# -----------------------------
class Bank:

    def __init__(self):
        self.accounts = LinkedList()

    def add_account(self, account):
        self.accounts.add(account)

    def __iter__(self):
        return iter(self.accounts)


# -----------------------------
# Objects
# -----------------------------
bank = Bank()
accounts = {}


# -----------------------------
# Create Account
# -----------------------------
def create_account():

    acc_no = input("Enter Account Number: ")

    if acc_no in accounts:
        print("Account Already Exists!")
        return

    name = input("Enter Holder Name: ")
    balance = float(input("Enter Initial Deposit: "))

    account = SavingsAccount(acc_no, name, balance)

    accounts[acc_no] = account
    bank.add_account(account)

    print("Account Created Successfully!")


# -----------------------------
# Deposit
# -----------------------------
def deposit_money():

    acc_no = input("Enter Account Number: ")

    if acc_no in accounts:

        amount = float(input("Enter Amount: "))
        accounts[acc_no].deposit(amount)

    else:
        print("Account Not Found!")


# -----------------------------
# Withdraw
# -----------------------------
def withdraw_money():

    acc_no = input("Enter Account Number: ")

    if acc_no in accounts:

        amount = float(input("Enter Amount: "))
        accounts[acc_no].withdraw(amount)

    else:
        print("Account Not Found!")


# -----------------------------
# Display Account
# -----------------------------
def display_account():

    acc_no = input("Enter Account Number: ")

    if acc_no in accounts:

        accounts[acc_no].display()

        print("\n------ Transaction Queue ------")

        if len(transaction_queue) == 0:
            print("No Transactions")

        else:
            for transaction in transaction_queue:
                print(transaction)

        print("\n------ Linked List (Iterator Output) ------")

        for account in bank:
            print(account.account_no, "-", account.holder_name)

        data = []

        for account in bank:

            data.append({

                "Account No": account.account_no,
                "Holder Name": account.holder_name,
                "Balance": account.get_balance()

            })

        df = pd.DataFrame(data)

        print("\n------ Account DataFrame ------")
        print(df)

    else:
        print("Account Not Found!")


# -----------------------------
# Admin Login
# -----------------------------
def admin_login():

    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin Login Successful!")
        admin_menu()

    else:
        print("Invalid Admin Credentials!")


# -----------------------------
# Admin: View All Accounts
# -----------------------------
def view_all_accounts():

    if bank.accounts.head is None:
        print("No Accounts Found!")
        return

    print("\n------ All Existing Accounts ------")

    for account in bank:
        account.display()

    data = []

    for account in bank:

        data.append({

            "Account No": account.account_no,
            "Holder Name": account.holder_name,
            "Balance": account.get_balance()

        })

    df = pd.DataFrame(data)

    print("\n------ All Accounts DataFrame ------")
    print(df)

    print("\nTotal Accounts :", len(data))
    print("Total Balance  : Rs.", df["Balance"].sum())


# -----------------------------
# Admin: Search Account
# -----------------------------
def admin_search_account():

    acc_no = input("Enter Account Number: ")

    if acc_no in accounts:
        accounts[acc_no].display()

    else:
        print("Account Not Found!")


# -----------------------------
# Admin: View All Transactions
# -----------------------------
def view_all_transactions():

    print("\n------ Transaction Queue ------")

    if len(transaction_queue) == 0:
        print("No Transactions")

    else:
        for transaction in transaction_queue:
            print(transaction)


# -----------------------------
# Admin Menu
# -----------------------------
def admin_menu():

    while True:

        print("\n========== ADMIN PANEL ==========")
        print("1. View All Accounts")
        print("2. Search Account Details")
        print("3. View All Transactions")
        print("4. Logout")

        choice = input("Enter Choice: ")

        if choice == "1":
            view_all_accounts()

        elif choice == "2":
            admin_search_account()

        elif choice == "3":
            view_all_transactions()

        elif choice == "4":
            print("Admin Logged Out!")
            break

        else:
            print("Invalid Choice!")


# -----------------------------
# Main Menu
# -----------------------------
while True:

    print("\n========== BANK MANAGEMENT SYSTEM ==========")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Display Account")
    print("5. Admin Login")
    print("6. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        deposit_money()

    elif choice == "3":
        withdraw_money()

    elif choice == "4":
        display_account()

    elif choice == "5":
        admin_login()

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("Invalid Choice!")