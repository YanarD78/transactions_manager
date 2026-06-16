# Finance Manager

A command-line application for tracking personal income and expenses, with user authentication and category-based statistics.

## Features

- Register and log in with a password (bcrypt hashing)
- Add transactions with type, amount, category and description
- View all transactions or filter by type or category
- Delete transactions
- View spending statistics by type or category

## Requirements

- Python 3.8+
- PostgreSQL
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

4. Create a PostgreSQL database and initialize the schema:
```bash
psql -U your_postgres_user -c "CREATE DATABASE your_database_name;"
psql -U your_postgres_user -d your_database_name -f schema.sql
```

5. Create a `.env` file in the project root:
```
DB_NAME=your_database_name
DB_USER=your_postgres_user
```

6. Run the application:
```bash
python main.py
```

## Usage

On launch, you will be prompted to log in or register. After authentication, the following commands are available:

- `add` — add a new transaction
- `transactions` — view, filter, delete transactions or show statistics
- `exit` — quit the application

### Transaction types
`income`, `expense`

### Categories
`food`, `transport`, `entertainment`, `health`, `communications`, `clothes and shoes`
