from decimal import Decimal, InvalidOperation
from Bank import Bank

def main():
    bank = Bank()
    print("Type 'help' for available commands.")
    
    def parse_decimal(s: str) -> Decimal:
        try:
            return Decimal(s)
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid amount format")
    
    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not user_input:
            continue
        parts = user_input.split()
        cmd = parts[0].lower()
        if cmd in ("exit", "quit"):
            print("Exiting.")
            break
        elif cmd == "help":
            print("""Available commands:
  create-account <name> <initial_balance>
  deposit <name> <amount>
  withdraw <name> <amount>
  transfer <from_name> <to_name> <amount>
  load-csv <filename>
  save-csv <filename>
  show
  exit""")
        elif cmd == "create-account":
            if len(parts) != 3:
                print("Usage: create-account <name> <initial_balance>")
            else:
                name = parts[1]
                try:
                    balance = parse_decimal(parts[2])
                    name = bank.create_account(name, balance)
                    print(f"Account created with name: {name}")
                except ValueError as e:
                    print(e)
        elif cmd == "deposit":
            if len(parts) != 3:
                print("Usage: deposit <name> <amount>")
            else:
                name = parts[1]
                try:
                    amount = parse_decimal(parts[2])
                    bank.deposit(name, amount)
                    print(f"Deposited {parts[2]} to account {name}")
                except ValueError as e:
                    print(e)
        elif cmd == "withdraw":
            if len(parts) != 3:
                print("Usage: withdraw <name> <amount>")
            else:
                name = parts[1]
                try:
                    amount = parse_decimal(parts[2])
                    bank.withdraw(name, amount)
                    print(f"Withdrew {parts[2]} from account {name}")
                except ValueError as e:
                    print(e)
        elif cmd == "transfer":
            if len(parts) != 4:
                print("Usage: transfer <from_name> <to_name> <amount>")
            else:
                from_name, to_name = parts[1], parts[2]
                try:
                    amount = parse_decimal(parts[3])
                    bank.transfer(from_name, to_name, amount)
                    print(f"Transferred {parts[3]} from {from_name} to {to_name}")
                except ValueError as e:
                    print(e)
        elif cmd == "load-csv":
            if len(parts) != 2:
                print("Usage: load-csv <filename>")
            else:
                filename = parts[1]
                try:
                    bank.load_from_csv(filename)
                    print(f"Accounts loaded from {filename}")
                except Exception as e:
                    print(e)
        elif cmd == "save-csv":
            if len(parts) != 2:
                print("Usage: save-csv <filename>")
            else:
                filename = parts[1]
                try:
                    bank.save_to_csv(filename)
                    print(f"Accounts saved to {filename}")
                except Exception as e:
                    print(e)
        elif cmd == "show":
            if len(parts) != 1:
                print("Usage: show")
            else:
                if not bank.accounts:
                    print("No accounts found.")
                else:
                    for name, account in bank.accounts.items():
                        print(f"{name}: {account.balance}")
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
