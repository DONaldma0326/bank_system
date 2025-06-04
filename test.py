import pytest
from decimal import Decimal
from Bank import Bank, BankAccount, InsufficientFundsError, AccountNotFoundError, NegativeAmountError

def test_create_account():
    bank = Bank()
    account_id = bank.create_account("Alice", Decimal('100.00'))
    account = bank.get_account(account_id)
    assert account.name == "Alice"
    assert account.balance == Decimal('100.00')

def test_create_account_negative_initial_balance():
    bank = Bank()
    with pytest.raises(NegativeAmountError):
        bank.create_account("Bob", Decimal('-50.00'))

def test_deposit():
    bank = Bank()
    account_id = bank.create_account("Charlie", Decimal('50.00'))
    bank.deposit(account_id, Decimal('25.00'))
    account = bank.get_account(account_id)
    assert account.balance == Decimal('75.00')

def test_deposit_negative_amount():
    bank = Bank()
    account_id = bank.create_account("David", Decimal('50.00'))
    with pytest.raises(NegativeAmountError):
        bank.deposit(account_id, Decimal('-10.00'))

def test_withdraw():
    bank = Bank()
    account_id = bank.create_account("Eve", Decimal('100.00'))
    bank.withdraw(account_id, Decimal('40.00'))
    account = bank.get_account(account_id)
    assert account.balance == Decimal('60.00')

def test_withdraw_insufficient_funds():
    bank = Bank()
    account_id = bank.create_account("Frank", Decimal('30.00'))
    with pytest.raises(InsufficientFundsError):
        bank.withdraw(account_id, Decimal('50.00'))

def test_withdraw_negative_amount():
    bank = Bank()
    account_id = bank.create_account("Grace", Decimal('30.00'))
    with pytest.raises(NegativeAmountError):
        bank.withdraw(account_id, Decimal('-5.00'))

def test_transfer():
    bank = Bank()
    from_account_id = bank.create_account("Hank", Decimal('100.00'))
    to_account_id = bank.create_account("Ivy", Decimal('50.00'))
    bank.transfer(from_account_id, to_account_id, Decimal('30.00'))
    from_account = bank.get_account(from_account_id)
    to_account = bank.get_account(to_account_id)
    assert from_account.balance == Decimal('70.00')
    assert to_account.balance == Decimal('80.00')

def test_transfer_insufficient_funds():
    bank = Bank()
    from_account_id = bank.create_account("Jack", Decimal('20.00'))
    to_account_id = bank.create_account("Kara", Decimal('50.00'))
    with pytest.raises(InsufficientFundsError):
        bank.transfer(from_account_id, to_account_id, Decimal('30.00'))

def test_transfer_negative_amount():
    bank = Bank()
    from_account_id = bank.create_account("Liam", Decimal('100.00'))
    to_account_id = bank.create_account("Mia", Decimal('50.00'))
    with pytest.raises(NegativeAmountError):
        bank.transfer(from_account_id, to_account_id, Decimal('-10.00'))

def test_transfer_same_account():
    bank = Bank()
    account_id = bank.create_account("Noah", Decimal('100.00'))
    with pytest.raises(ValueError):
        bank.transfer(account_id, account_id, Decimal('10.00'))

def test_get_account_not_found():
    bank = Bank()
    with pytest.raises(AccountNotFoundError):
        bank.get_account("non-existent-id")
