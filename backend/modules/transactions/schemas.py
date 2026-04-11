import json
from pydantic import BaseModel
from typing import Any, Literal

from .models import TransactionORM


class Transaction(BaseModel):
    transaction_type: Literal["income", "expense", "internal"]
    account_name: str
    date: Any
    category: str = "Undefined"
    amount: int

    def to_orm(self) -> TransactionORM:
        return TransactionORM(**self.model_dump())
