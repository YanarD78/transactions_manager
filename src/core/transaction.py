from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Transaction:
    type: str
    amount: Decimal
    category: str
    user_id: int
    description: str = None