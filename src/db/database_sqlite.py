import sqlite3
from pathlib import Path
from src.db.base import BaseDBManager, db_error_handler

class DBmanager(BaseDBManager):
    def __init__(self, db_name):
        db_path = Path(db_name).resolve()
        db_exists = db_path.exists()
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")
        if not db_exists:
            self._create()

    def drop_connection(self):
        if self.connection:
            self.connection.close()

    def drop_cursor(self):
        if self.cursor:
            self.cursor.close()

    @db_error_handler
    def add_transaction(self, transaction):
        sql_query = ("INSERT INTO transactions (type, amount, category, description, user_id) VALUES (?, ?, ?, ?, ?)")
        self.cursor.execute(sql_query, (transaction.type, str(transaction.amount), transaction.category, transaction.description, transaction.user_id))
        self.connection.commit()

    @db_error_handler
    def delete_transaction(self, number_of, user_id):
        self.cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (number_of, user_id))
        self.connection.commit()

    @db_error_handler
    def statistic_type(self, user_id):
        self.cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type", (user_id,))
        return self.cursor.fetchall()

    @db_error_handler
    def statistic_category(self, user_id):
        self.cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY category", (user_id,))
        return self.cursor.fetchall()

    @db_error_handler
    def add_user(self, username, hashed):
        try:
            sql_query = "INSERT INTO users (username, hash) VALUES (?, ?)"
            self.cursor.execute(sql_query, (username, hashed))
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError("This username is already taken. Choose another one")

    @db_error_handler
    def find_user(self, username):
        sql_query = "SELECT * FROM users WHERE username = ?"
        self.cursor.execute(sql_query, (username,))
        result = self.cursor.fetchall()
        if not result:
            return None
        return result[0]

    @db_error_handler
    def get_all_transactions(self, user_id):
        self.cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    @db_error_handler
    def get_transactions_category(self, category, user_id):
        query = "SELECT * FROM transactions WHERE category = ? AND user_id = ?"
        self.cursor.execute(query, (category, user_id))
        records = self.cursor.fetchall()
        return records
    
    @db_error_handler
    def get_transactions_type(self, type_of, user_id):
        query = "SELECT * FROM transactions WHERE type = ? AND user_id = ?"
        self.cursor.execute(query, (type_of, user_id))
        records = self.cursor.fetchall()
        return records
    


    def _create(self):
        schema_path = Path(__file__).parent / 'schema_sqlite.sql'
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found at: {schema_path.resolve()}")
        with open(schema_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        self.cursor.executescript(sql_script)
        self.connection.commit()