
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Transaction, User
from schemas import TransactionCreate, TransactionResponse
from finauth import get_current_user
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# GET all transactions (only yours)
@router.get("/", response_model=List[TransactionResponse])
def get_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).all()

# GET single transaction
@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    t = db.query(Transaction).filter(Transaction.id == id, Transaction.user_id == current_user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return t

# POST create new transaction
@router.post("/", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    t = Transaction(**data.dict(), user_id=current_user.id)
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

# PUT update transaction
@router.put("/{id}", response_model=TransactionResponse)
def update_transaction(id: int, data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    t = db.query(Transaction).filter(Transaction.id == id, Transaction.user_id == current_user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in data.dict().items():
        setattr(t, key, value)
    db.commit()
    db.refresh(t)
    return t

# DELETE transaction
@router.delete("/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    t = db.query(Transaction).filter(Transaction.id == id, Transaction.user_id == current_user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(t)
    db.commit()
    return {"message": "Deleted successfully"}