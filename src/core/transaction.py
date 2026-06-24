from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Transaction:
    type: str
    amount: Decimal
    category: str
    user_id: int
    description: str = None
    id: int = None
    created_at: str = None

    @classmethod
    def from_row(cls, row):
        return cls(
            id = row[0],
            type = row[1],
            amount = Decimal(row[2]),
            category = row[3],
            description = row[4],
            created_at = row[5],
            user_id = row[6]
        )