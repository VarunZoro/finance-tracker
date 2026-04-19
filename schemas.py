from pydantic import BaseModel, field_validator
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

    @field_validator('title')
    def title_must_be_valid(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title too long')
        return v.strip()

    @field_validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if v > 10000000:
            raise ValueError('Amount too large')
        return v

    @field_validator('type')
    def type_must_be_valid(cls, v):
        if v not in ['income', 'expense']:
            raise ValueError('Type must be income or expense')
        return v

    @field_validator('notes')
    def notes_length(cls, v):
        if v and len(v) > 500:
            raise ValueError('Notes too long')
        return v

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

    @field_validator('username')
    def username_must_be_valid(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Username must be at least 3 characters')
        if len(v) > 50:
            raise ValueError('Username too long')
        return v.strip()

    @field_validator('password')
    def password_must_be_valid(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        if len(v) > 72:
            raise ValueError('Password too long')
        return v

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str