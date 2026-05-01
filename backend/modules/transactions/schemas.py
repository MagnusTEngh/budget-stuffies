import json
from pydantic import BaseModel
from typing import Any, Literal
from datetime import date
from .models import TransactionORM


class Transaction(BaseModel):
    transaction_type: Literal["income", "expense", "internal"]
    account_name: str
    date: date
    category: str = "Undefined"
    amount: int

    def to_orm(self) -> TransactionORM:
        return TransactionORM(**self.model_dump())
