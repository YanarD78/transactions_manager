import psycopg2

def db_error_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception:
            if self.connection:
                self.connection.rollback()
            raise
    return wrapper

class DBmanager:
    def __init__(self, db_name, user, password=None, host="localhost", port=5432):
        try:
            self.connection = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
            )
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Database connection failed: {e.args[0].strip()}")
        self.cursor = self.connection.cursor()
    
    def drop_connection(self):
        if self.connection:
            self.connection.close()
    def drop_cursor(self):
        if self.cursor:
            self.cursor.close()

    @db_error_handler
    def add_transaction(self, transaction):
        sql_query = ("INSERT INTO transactions (type, amount, category, description, user_id) VALUES (%s, %s, %s, %s, %s)")
        self.cursor.execute(sql_query, (transaction.type, transaction.amount, transaction.category, transaction.description, transaction.user_id))
        self.connection.commit()

    @db_error_handler
    def delete_transaction(self, number_of, user_id):
        self.cursor.execute("DELETE FROM transactions WHERE id = %s AND user_id = %s", (number_of, user_id))
        self.connection.commit()

    @db_error_handler
    def statistic_type(self, user_id):
        self.cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY type", (user_id,))
        return self.cursor.fetchall()

    @db_error_handler
    def statistic_category(self, user_id):
        self.cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY category", (user_id,))
        return self.cursor.fetchall()

    @db_error_handler
    def add_user(self, username, hashed):
        sql_query = "INSERT INTO users (username, hash) VALUES (%s, %s)"
        self.cursor.execute(sql_query, (username, hashed))
        self.connection.commit()

    @db_error_handler
    def find_user(self, username):
        sql_query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(sql_query, (username,))
        result = self.cursor.fetchall()
        if not result:
            return None
        return result[0]

    @db_error_handler
    def get_all_transactions(self, user_id):
        self.cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    @db_error_handler
    def get_transactions_category(self, category, user_id):
        query = "SELECT * FROM transactions WHERE category = %s AND user_id = %s"
        self.cursor.execute(query, (category, user_id))
        records = self.cursor.fetchall()
        return records
    
    @db_error_handler
    def get_transactions_type(self, type_of, user_id):
        query = "SELECT * FROM transactions WHERE type = %s AND user_id = %s"
        self.cursor.execute(query, (type_of, user_id))
        records = self.cursor.fetchall()
        return records