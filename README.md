# BankSystem

## Overview

BankSystem is a Python application for processing CSV data, providing functionality to load data from a CSV file, apply custom functions, save the results to a new CSV, and run tests to ensure correctness.

## Prerequisites

- Python 3.8 or higher
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<username>/BankSystem.git
   cd BankSystem
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .\.venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Follow these steps to run and interact with the application:

### 1. Start the Application

Run the main entry point:
```bash
python main.py
```

### 2. Call the Processing Function

Invoke the core processing function with any required arguments:
```bash
python main.py --function <function_name> [--args]
```

### 3. Load CSV Data

Load input data from a CSV file:
```bash
python main.py --load-csv path/to/input.csv
```

### 4. Save CSV Data

Save processed data to a new CSV file:
```bash
python main.py --save-csv path/to/output.csv
```

## Running Tests

Execute the test suite to verify functionality:
```bash
pytest
```

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.