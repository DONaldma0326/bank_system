import csv
import os
from typing import Dict, Optional
from decimal import Decimal, InvalidOperation
import uuid

class InsufficientFundsError(Exception):
    pass

class AccountNotFoundError(Exception):
    pass

class NegativeAmountError(Exception):
    pass

class BankAccount:
    def __init__(self, account_id: str, name: str, balance: Decimal):
        self.account_id = account_id
        self.name = name
        self.balance = balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise NegativeAmountError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise NegativeAmountError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Insufficient funds for withdrawal")
        self.balance -= amount

    def to_dict(self) -> Dict[str, str]:
        return {
            'account_id': self.account_id,
            'name': self.name,
            'balance': str(self.balance)
        }

class Bank:
    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}

    def create_account(self, name: str, initial_balance: Decimal = Decimal('0')) -> str:
        if initial_balance < 0:
            raise NegativeAmountError("Initial balance cannot be negative")
        account_id = str(uuid.uuid4())
        self.accounts[account_id] = BankAccount(account_id, name, initial_balance)
        print(f"Account {account_id} created with initial balance {initial_balance}")
        return account_id

    def get_account(self, account_id: str) -> BankAccount:
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Account {account_id} not found")
        return self.accounts[account_id]

    def deposit(self, account_id: str, amount: Decimal) -> None:
        account = self.get_account(account_id)
        account.deposit(amount)

    def withdraw(self, account_id: str, amount: Decimal) -> None:
        account = self.get_account(account_id)
        account.withdraw(amount)

    def transfer(self, from_account_id: str, to_account_id: str, amount: Decimal) -> None:
        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account")
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        # Ensure atomicity: check balance first, then perform operations
        if amount <= 0:
            raise NegativeAmountError("Transfer amount must be positive")
        if from_account.balance < amount:
            raise InsufficientFundsError("Insufficient funds for transfer")
        
        from_account.balance -= amount
        to_account.balance += amount

    def save_to_csv(self, filename: str) -> None:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['account_id', 'name', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self.accounts.values():
                writer.writerow(account.to_dict())

    def load_from_csv(self, filename: str) -> None:
        if not os.path.exists(filename):
            return
        self.accounts.clear()
        seen_ids = set()
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                account_id = row['account_id']
                if account_id in seen_ids:
                    raise ValueError(f"Duplicate account_id {account_id} in CSV")
                try:
                    balance = Decimal(row['balance'])
                except InvalidOperation:
                    raise ValueError(f"Invalid balance format for account {account_id}")
                if balance < 0:
                    raise ValueError(f"Negative balance {balance} for account {account_id}")
                seen_ids.add(account_id)
                self.accounts[account_id] = BankAccount(
                    account_id,
                    row['name'],
                    balance
                )
                
