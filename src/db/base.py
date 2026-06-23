from abc import ABC, abstractmethod
from functools import wraps

def db_error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception:
            if self.connection:
                self.connection.rollback()
            raise
    return wrapper



class BaseDBManager(ABC):
    @abstractmethod
    def drop_connection(self):
        """close connection"""

    @abstractmethod
    def drop_cursor(self):
        """close cursor"""

    @abstractmethod
    def add_transaction(self, transaction):
        """add transaction"""

    @abstractmethod
    def delete_transaction(self, number_of, user_id):
        """delete transaction"""

    @abstractmethod
    def statistic_type(self, user_id):
        """statisic by type"""

    @abstractmethod
    def statistic_category(self, user_id):
        """statistic by category"""

    @abstractmethod
    def add_user(self, username, hashed):
        """registration"""

    @abstractmethod
    def find_user(self, username):
        """authorization"""

    @abstractmethod
    def get_all_transactions(self, user_id):
        """show all transactions"""

    @abstractmethod
    def get_transactions_category(self, category, user_id):
        """show transactions by category"""
        
    @abstractmethod
    def get_transactions_type(self, type_of, user_id):
        """show transactions by category""" 