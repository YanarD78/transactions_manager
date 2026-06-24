# Finance Manager

A command-line application for tracking personal income and expenses. Supports two database backends — SQLite (default) and PostgreSQL — switchable via a CLI flag.

## Features

- User registration and login with bcrypt password hashing
- Add transactions with type, amount, category, and description
- View all transactions or filter by type / category
- Delete transactions by number
- Spending statistics grouped by type or category

## Requirements

- Python 3.8+
- PostgreSQL (only if using the `--db postgres` flag)
- Dependencies listed in `requirements.txt`

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YanarD78/transactions_manager.git
cd transactions_manager
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. *(PostgreSQL only)* Create a database, initialize the schema, and create a `.env` file:
```bash
psql -U your_user -c "CREATE DATABASE your_db;"
psql -U your_user -d your_db -f src/db/schema.sql
```
```env
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
```

## Running

SQLite is used by default — no configuration needed:
```bash
python main.py
```

To use PostgreSQL:
```bash
python main.py --db postgres
```

## Usage

On launch you will be prompted to log in or register. After authentication:

| Command | Description |
|---|---|
| `add` | Add a new transaction |
| `transactions` | View, filter, delete transactions or show statistics |
| `exit` | Quit the application |

Under `transactions`, available options are: `all`, `type`, `category`, `delete`, `statistic`.

### Transaction types
`income`, `expense`

### Categories
`food`, `transport`, `entertainment`, `health`, `communications`, `clothes and shoes`

## Project Structure

```
src/
├── clients/
│   └── cli/        # Terminal interface
├── core/
│   ├── manager.py  # Business logic
│   └── transaction.py
└── db/
    ├── base.py     # Abstract DB interface
    ├── database.py         # PostgreSQL implementation
    └── database_sqlite.py  # SQLite implementation
```