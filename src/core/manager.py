import bcrypt
from decimal import Decimal, InvalidOperation
from src.core.transaction import Transaction

class Manager:
    VALID_CATEGORIES = frozenset({
    "food", "transport", "entertainment", 
    "health", "communications", "clothes and shoes"
    })
        
    def __init__(self, database):
        self.database = database
        self.user_id = None

    def add_user(self, username, password):
        if len(username) < 6:
            raise ValueError("Username must be at least 6 characters long")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        bytes_password = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(bytes_password, salt)
        hashed_str = hashed.decode('utf-8')
        try:
            self.database.add_user(username, hashed_str)
        except ValueError as e:
            raise ValueError(e)

    def login(self, username, password):
        user = self.database.find_user(username)
        if user is not None:
            if bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                self.user_id = user[0]
                return self.user_id
            else:
                raise ValueError("Invalid username or password")
        else:
            raise ValueError("Invalid username or password")

    def get_all_transactions(self):
        rows = self.database.get_all_transactions(self.user_id) or []
        return [Transaction.from_row(row) for row in rows]

    def get_transactions(self, value, kind):
        if value == "category":
            rows = self.database.get_transactions_category(kind, self.user_id)
        elif value == "type_of":
            rows = self.database.get_transactions_type(kind, self.user_id)
        else:
            return None
        return [Transaction.from_row(row) for row in rows]
        
    def statistic(self, filter_by):
        if filter_by == "type":
            return self.database.statistic_type(self.user_id)
        elif filter_by == "category":
            return self.database.statistic_category(self.user_id)
        else:
            return None
        
    def delete_transaction(self, choice):
        rows = self.database.get_all_transactions(self.user_id) or []
        transactions = [Transaction.from_row(row) for row in rows]
        try:
            number = int(choice)
        except ValueError:
            raise ValueError("Invalid input. Please enter a valid transaction number")
        if not (1 <= number <= len(transactions)):
            raise ValueError("Transaction number out of range")
        else:
            choosen = transactions[number - 1]
            transaction_id = choosen.id
            self.database.delete_transaction(transaction_id, self.user_id)
    
    def add_transaction(self, transaction_type, amount, category, description):
        if transaction_type not in ("expense", "income"):
            raise ValueError("Invalid transaction type. Choose 'income' or 'expense'")
        try:
            amount = Decimal(amount)
        except ValueError:
            raise ValueError("Invalid amount. Please enter a valid number")
        except InvalidOperation:
            raise TypeError("Invalid amount. Please enter a valid value")
        if amount <= 0:
            raise ValueError("Invalid amount. Please enter a valid number")

        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Invalid category. Choose from: {', '.join(self.VALID_CATEGORIES)}.")
        else:
            transaction = Transaction(transaction_type, amount, category, self.user_id, description)
            self.database.add_transaction(transaction)