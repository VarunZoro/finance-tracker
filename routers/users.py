from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from finauth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

# Register
@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = User(username=data.username, password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Login
@router.post("/login", response_model=Token)
def login(data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}