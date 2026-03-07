
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Transaction
from schemas import TransactionCreate, TransactionResponse
from typing import List

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# sabhi transactions lene ke liye
@router.get("/", response_model=List[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

# ek transaction lene ke liye id se
@router.get("/{id}", response_model=TransactionResponse)
def get_transaction(id: int, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return t

# naya transaction banane ke liye
@router.post("/", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    t = Transaction(**data.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

# transaction update karne ke liye
@router.put("/{id}", response_model=TransactionResponse)
def update_transaction(id: int, data: TransactionCreate, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    for key, value in data.dict().items():
        setattr(t, key, value)
    db.commit()
    db.refresh(t)
    return t

# transaction delete karne ke liye
@router.delete("/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    t = db.query(Transaction).filter(Transaction.id == id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(t)
    db.commit()
    return {"message": "Deleted successfully"}