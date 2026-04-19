from fastapi import APIRouter, Depends, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from finauth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
limiter = Limiter(key_func=get_remote_address)

# Register
@router.post("/register", response_model=UserResponse)
@limiter.limit("5/15minutes")
def register(request: Request, data: UserCreate, db: Session = Depends(get_db)):
    # Sanitize inputs
    if len(data.username) > 50:
        raise HTTPException(status_code=400, detail="Username too long")
    if len(data.password) > 72:
        raise HTTPException(status_code=400, detail="Password too long")
    if len(data.username) < 3:
        raise HTTPException(status_code=400, detail="Username too short")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")

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
@limiter.limit("5/15minutes")
def login(request: Request, data: UserCreate, db: Session = Depends(get_db)):
    # Sanitize inputs
    if len(data.username) > 50 or len(data.password) > 72:
        raise HTTPException(status_code=400, detail="Input too long")

    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}