# Personal Expense Tracker

A console-based personal finance application built with Python. It allows users to record income and expenses, review transactions, search and filter records, and generate monthly summaries.

## Features

- Add income and expense transactions
- Choose an expense category
- View all saved transactions
- Calculate total income, total expenses, and current balance
- Search transactions by description
- Filter transactions by category
- Delete a transaction
- Generate a monthly report with category breakdown
- Save and load records automatically using JSON

## Technologies

- Python 3
- JSON for local data storage
- Python standard library (`json`, `os`, `datetime`, `collections`)

## Requirements

Python 3. No third-party packages are required.

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python expense_tracker.py
   ```

   On some systems, use:

   ```bash
   python3 expense_tracker.py
   ```

4. Follow the on-screen menu.

The application creates `expenses.json` automatically when the first transaction is saved. Keep this file in the same folder as the Python program so your records can be loaded the next time you run it.

## Menu

| Option | Action |
|---|---|
| 1 | Add income |
| 2 | Add expense |
| 3 | View all transactions |
| 4 | View financial summary |
| 5 | Search transactions |
| 6 | Filter by category |
| 7 | Delete a transaction |
| 8 | View monthly report |
| 9 | Exit |

## Data Format

Transactions are stored locally in `expenses.json`. Each record contains an ID, transaction type, amount, description, category, and date.

Example:

```json
{
  "id": 1,
  "type": "Expense",
  "amount": 120.0,
  "description": "Lunch",
  "category": "Food",
  "date": "2026-11-01"
}
```

## Notes and Limitations

- This is an educational project and is not intended to replace professional accounting software.
- Data is stored locally in a JSON file, not in an online database.
- Back up `expenses.json` if you want to keep your records safe.
- The program uses a simple transaction ID system. A future version could use unique IDs, stronger data validation, and automated unit tests.

## Future Improvements

- Add CSV export
- Add budget limits and spending alerts
- Add charts for monthly spending
- Add a graphical user interface
- Add automated unit tests
- Use unique transaction IDs and backup handling

Author: [Hein Zin Htut]  
Project: Expense Tracker  
Language: Python 3
