from dataclasses import dataclass

@dataclass
class Transaction:
    type: str
    amount: float
    category: str
    user_id: int
    description: str = None