Version
Python 3.8 or higher


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<username>/BankSystem.git
   cd BankSystem
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  #mac os / linux 
   .\.venv\\Scripts\\activate # On Windows use
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application in interactive mode:
```bash
python main.py
```

At the prompt, enter one of the following commands:
- create-account <name> <initial_balance>
- deposit <account_name> <amount>
- withdraw <account_name> <amount>
- transfer <from_account_name> <to_account_name> <amount>
- load-csv <filename>
- save-csv <filename>
- help
- show
- exit

## Running Tests and Coverage

Run all tests:

```bash
python test.py
```
which executes tests and prints a coverage report.

