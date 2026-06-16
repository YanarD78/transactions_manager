class Transaction:
    def __init__(self, transaction_type, amount, category, user_id, description = None):
        self.type = transaction_type
        self.amount = amount
        self.category = category
        self.user_id = user_id
        self.description = description