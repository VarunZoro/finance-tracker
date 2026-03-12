from pydantic import BaseModel
from datetime import date
from typing import Optional

# ── Transaction Schemas ──
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
    user_id: int

    class Config:
        from_attributes = True

# ── User Schemas ──
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
