import csv
import os
from typing import Dict
from decimal import Decimal, InvalidOperation



class BankAccount:
    def __init__(self,name: str, balance: float):
        self.name = name
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        print(f"Deposited {amount} to {self.name}. New balance: {self.balance}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal")
        self.balance -= amount
        print(f"Withdrew {amount} from {self.name}. New balance: {self.balance}")
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'name': self.name,
            'balance': str(self.balance)
        }

class Bank:
    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}

    def create_account(self, name: str, initial_balance: float = float('0')) -> str:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        if name in self.accounts:
            raise ValueError("Account name must be unique")
        self.accounts[name] = BankAccount(name, initial_balance)
        return name

    def get_account(self, name: str) -> BankAccount:
        if name not in self.accounts:
            raise ValueError(f"Account {name} not found")
        return self.accounts[name]

    def deposit(self, name: str, amount: float) -> None:
        account = self.get_account(name)
        account.deposit(amount)

    def withdraw(self, name: str, amount: float) -> None:
        account = self.get_account(name)
        account.withdraw(amount)

    def transfer(self, from_name: str, to_name: str, amount: float) -> None:
        if from_name == to_name:
            raise ValueError("Cannot transfer to the same account")
        from_account = self.get_account(from_name)
        to_account = self.get_account(to_name)
        
        # Ensure atomicity: check balance first, then perform operations
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if from_account.balance < amount:
            raise ValueError("Insufficient funds for transfer")
        
        from_account.balance -= amount
        to_account.balance += amount
    def save_to_csv(self, filename: str) -> None:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self.accounts.values():
                writer.writerow(account.to_dict())
    def load_from_csv(self, filename: str) -> None:
        if not os.path.exists(filename):
            return
        self.accounts.clear()
        seen_names = set()
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name']
                if name in seen_names:
                    raise ValueError(f"Duplicate name {name} in CSV")
                raw_balance = row['balance']
                try:
                    balance = float(raw_balance)
                except ValueError:
                    raise ValueError(f"Invalid balance format for account {name}")
                if balance < 0:
                    raise ValueError(f"Negative balance {raw_balance} for account {name}")
                seen_names.add(name)
                self.accounts[name] = BankAccount(
                    name,
                    balance
                )
        