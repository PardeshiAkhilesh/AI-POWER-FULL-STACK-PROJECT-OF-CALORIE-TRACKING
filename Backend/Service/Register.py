from fastapi import APIRouter, Depends, Request, status,HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta,datetime,timezone

from Database.sql import get_db
from Schema.Auth import RegisterRequest, TokenResponse, LoginRequest
from Models.register import User
from Utils.jwt_token import create_access_token, create_refresh_token
import secrets
import hashlib
from Utils.constancs import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

def generate_refresh_token() -> str:
    """Generate secure random refresh token."""
    return secrets.token_urlsafe(48)

def get_utc_now():
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


@router.post("/register",status_code=status.HTTP_201_CREATED)
def register_user(data: RegisterRequest,db: Session = Depends(get_db)):
    """Register a new user"""
    if data.password != data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Enail is already registered")
    
    user = User(
        email = data.email,
        fullname = data.full_name,
        hashpassword = hash_password(data.password),
        provider = "local",
        is_active = True
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")
    
    #access_token = create_access_token({"sub": str(user.id)})
    #refresh_token = generate_refresh_token()
    #save_refresh_token(db,user.id,refresh_token)

    return "User registered successfully"

@router.post("/login")
def login(data: LoginRequest, db:Session = Depends(get_db)):
    if not data.email or not data.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email and password are required")
    
    user = db.query(User).filter(User.email == data.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    if not verify_password(data.password, user.hashpassword):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    
    return "Login successfully"

    



        
def save_refresh_token(db: Session, user_id: int, token:str):
    expires_at = get_utc_now() + timedelta(days=7)
    refresh = User.RefreshToken(token=token,user_id=user_id,expires_at=expires_at,is_revoked=False)

    try:
        db.add(refresh)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save refresh token")
    


    