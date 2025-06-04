import argparse
from decimal import Decimal
from Bank import Bank, InsufficientFundsError, AccountNotFoundError, NegativeAmountError

def main():
    parser = argparse.ArgumentParser(description="Bank System Command Line Interface")
    parser.add_argument('--create-account', nargs=2, metavar=('name', 'initial_balance'), help='Create a new bank account')
    parser.add_argument('--deposit', nargs=2, metavar=('account_id', 'amount'), help='Deposit amount into an account')
    parser.add_argument('--withdraw', nargs=2, metavar=('account_id', 'amount'), help='Withdraw amount from an account')
    parser.add_argument('--transfer', nargs=3, metavar=('from_account_id', 'to_account_id', 'amount'), help='Transfer amount between accounts')
    parser.add_argument('--save-csv', metavar='filename', help='Save accounts to a CSV file')
    parser.add_argument('--load-csv', metavar='filename', help='Load accounts from a CSV file')

    args = parser.parse_args()
    bank = Bank()

    if args.load_csv:
        bank.load_from_csv(args.load_csv)
        print(f"Accounts loaded from {args.load_csv}")

    if args.create_account:
        name, initial_balance = args.create_account
        try:
            account_id = bank.create_account(name, Decimal(initial_balance))
            print(f"Account created with ID: {account_id}")
        except NegativeAmountError as e:
            print(e)

    if args.deposit:
        account_id, amount = args.deposit
        try:
            bank.deposit(account_id, Decimal(amount))
            print(f"Deposited {amount} to account {account_id}")
        except (AccountNotFoundError, NegativeAmountError) as e:
            print(e)

    if args.withdraw:
        account_id, amount = args.withdraw
        try:
            bank.withdraw(account_id, Decimal(amount))
            print(f"Withdrew {amount} from account {account_id}")
        except (AccountNotFoundError, NegativeAmountError, InsufficientFundsError) as e:
            print(e)

    if args.transfer:
        from_account_id, to_account_id, amount = args.transfer
        try:
            bank.transfer(from_account_id, to_account_id, Decimal(amount))
            print(f"Transferred {amount} from {from_account_id} to {to_account_id}")
        except (AccountNotFoundError, NegativeAmountError, InsufficientFundsError, ValueError) as e:
            print(e)

    if args.save_csv:
        bank.save_to_csv(args.save_csv)
        print(f"Accounts saved to {args.save_csv}")

if __name__ == "__main__":
    main()
