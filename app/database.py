import psycopg2

class DBmanager:
    def __init__(self, db_name, user, password=None, host="localhost", port=5432):
        self.connection = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
    
    def drop_connection(self):
        if self.connection:
            self.connection.close()
    def drop_cursor(self):
        if self.cursor:
            self.cursor.close()

    def add_transaction(self, transaction):
        sql_query = ("INSERT INTO transactions (type, amount, category, description, user_id) VALUES (%s, %s, %s, %s, %s)")
        self.cursor.execute(sql_query, (transaction.type, transaction.amount, transaction.category, transaction.description, transaction.user_id))
        self.connection.commit()

    def delete_transaction(self, number_of, user_id):
        self.cursor.execute("DELETE FROM transactions WHERE id = %s AND user_id = %s", (number_of, user_id))
        self.connection.commit()

    def statistic_type(self, user_id):
        self.cursor.execute("SELECT type, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY type", (user_id,))
        return self.cursor.fetchall()

    def statistic_category(self, user_id):
        self.cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE user_id = %s GROUP BY category", (user_id,))
        return self.cursor.fetchall()

    def add_user(self, username, hashed):
        sql_query = "INSERT INTO users (username, hash) VALUES (%s, %s)"
        self.cursor.execute(sql_query, (username, hashed))
        self.connection.commit()

    def find_user(self, username):
        sql_query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(sql_query, (username,))
        result = self.cursor.fetchall()
        if not result:
            return None
        return result[0]

    def get_all_transactions(self, user_id):
        self.cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
        return self.cursor.fetchall()

    def get_transactions_category(self, category, user_id):
        query = "SELECT * FROM transactions WHERE category = %s AND user_id = %s"
        self.cursor.execute(query, (category, user_id))
        records = self.cursor.fetchall()
        return records
    
    def get_transactions_type(self, type_of, user_id):
        query = "SELECT * FROM transactions WHERE type = %s AND user_id = %s"
        self.cursor.execute(query, (type_of, user_id))
        records = self.cursor.fetchall()
        return records