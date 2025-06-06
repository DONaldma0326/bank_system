import pytest
from decimal import Decimal
import sys
import coverage
from Bank import Bank, BankAccount

def test_create_account():
    bank = Bank()
    account_name = bank.create_account("Alice", float('100.00'))
    account = bank.get_account(account_name)
    assert account.name == "Alice"
    assert account.balance == float('100.00')

def test_create_account_negative_initial_balance():
    bank = Bank()
    with pytest.raises(ValueError):
        bank.create_account("Bob", float('-50.00'))

def test_deposit():
    bank = Bank()
    account_name = bank.create_account("Charlie", float('50.00'))
    bank.deposit(account_name, float('25.00'))
    account = bank.get_account(account_name)
    assert account.balance == float('75.00')

def test_deposit_negative_amount():
    bank = Bank()
    account_name = bank.create_account("David", float('50.00'))
    with pytest.raises(ValueError):
        bank.deposit(account_name, float('-10.00'))

def test_withdraw():
    bank = Bank()
    account_name = bank.create_account("Eve", float('100.00'))
    bank.withdraw(account_name, float('40.00'))
    account = bank.get_account(account_name)
    assert account.balance == float('60.00')

def test_withdraw_insufficient_funds():
    bank = Bank()
    account_name = bank.create_account("Frank", float('30.00'))
    with pytest.raises(ValueError):
        bank.withdraw(account_name, float('50.00'))

def test_withdraw_negative_amount():
    bank = Bank()
    account_name = bank.create_account("Grace", float('30.00'))
    with pytest.raises(ValueError):
        bank.withdraw(account_name, float('-10.00'))

def test_transfer():
    bank = Bank()
    from_account_name = bank.create_account("Hank", float('100.00'))
    to_account_name = bank.create_account("Ivy", float('50.00'))
    bank.transfer(from_account_name, to_account_name, float('30.00'))
    from_account = bank.get_account(from_account_name)
    to_account = bank.get_account(to_account_name)
    assert from_account.balance == float('70.00')
    assert to_account.balance == float('80.00')

def test_transfer_insufficient_funds():
    bank = Bank()
    from_account_name = bank.create_account("Jack", float('20.00'))
    to_account_name = bank.create_account("Kara", float('50.00'))
    with pytest.raises(ValueError):
        bank.transfer(from_account_name, to_account_name, float('30.00'))

def test_transfer_negative_amount():
    bank = Bank()
    from_account_name = bank.create_account("Liam", float('100.00'))
    to_account_name = bank.create_account("Mia", float('50.00'))
    with pytest.raises(ValueError):
        bank.transfer(from_account_name, to_account_name, float('-10.00'))

def test_transfer_same_account():
    bank = Bank()
    name = bank.create_account("Noah", float('100.00'))
    with pytest.raises(ValueError):
        bank.transfer(name, name, float('10.00'))

def test_get_account_not_found():
    bank = Bank()
    with pytest.raises(ValueError):
        bank.get_account("non-existent-id")

def test_save_and_load_csv(tmp_path):
    bank = Bank()
    name1 = bank.create_account("A", float('5.00'))
    name2 = bank.create_account("B", float('7.50'))
    file = tmp_path / "accounts.csv"
    bank.save_to_csv(str(file))
    bank2 = Bank()
    bank2.load_from_csv(str(file))
    acct1 = bank2.get_account(name1)
    acct2 = bank2.get_account(name2)
    assert acct1.name == "A"
    assert acct1.balance == float('5.00')
    assert acct2.name == "B"
    assert acct2.balance == float('7.50')

def test_load_nonexistent_csv(tmp_path):
    bank = Bank()
    name1 = bank.create_account("C", float('3.00'))
    nonfile = tmp_path / "noexist.csv"
    if nonfile.exists():
        nonfile.unlink()
    bank.load_from_csv(str(nonfile))
    acct = bank.get_account(name1)
    assert acct.name == "C"
    assert acct.balance == float('3.00')

def test_load_csv_duplicate_name(tmp_path):
    file = tmp_path / "dup.csv"
    file.write_text("name,balance\nx,10.00\nx,20.00\n")
    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        bank.load_from_csv(str(file))
    assert "Duplicate name x" in str(excinfo.value)

def test_load_csv_invalid_balance(tmp_path):
    file = tmp_path / "inv.csv"
    file.write_text("name,balance\ny,notnumber\n")
    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        bank.load_from_csv(str(file))
    assert "Invalid balance format for account y" in str(excinfo.value)

def test_load_csv_negative_balance(tmp_path):
    file = tmp_path / "neg.csv"
    file.write_text("name,balance\nz,-5.00\n")
    bank = Bank()
    with pytest.raises(ValueError) as excinfo:
        bank.load_from_csv(str(file))
    assert "Negative balance -5.0" in str(excinfo.value)

def test_load_clears_existing_accounts(tmp_path):
    bank1 = Bank()
    id_old = bank1.create_account("Old", float('1.00'))
    file = tmp_path / "clear.csv"
    bank1.save_to_csv(str(file))
    id_new = bank1.create_account("New", float('2.00'))
    bank1.load_from_csv(str(file))
    with pytest.raises(ValueError):
        bank1.get_account(id_new)
    acct = bank1.get_account(id_old)
    assert acct.name == "Old"
    assert acct.balance == float('1.00')

if __name__ == "__main__":
    cov = coverage.Coverage(source=["Bank"])
    cov.start()
    exit_code = pytest.main([__file__])
    cov.stop()
    cov.save()
    print("\nCoverage Report:")
    cov.report(show_missing=True)
    sys.exit(exit_code)
