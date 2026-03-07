from pydantic import BaseModel
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    title: str
    amount: float
    category: str
    type: str
    date: date
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int

    class config:
        from_attributes = True


