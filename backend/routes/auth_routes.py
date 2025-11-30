from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database.models import User
from backend.utils.password_hashing import verify_password, hash_password

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    
    dummy_hash = hash_password("dummy123")  # timing mitigation
    if not user or not verify_password(request.password, user.password_hash if user else dummy_hash):
        return JSONResponse({"status": "error", "message": "Invalid credentials"})
    
    return JSONResponse({"status": "ok", "message": "Login successful"})


class SignupRequest(BaseModel):
    username: str
    password: str
@router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    
    # Check if username exists
    if db.query(User).filter(User.username == request.username).first():
        return JSONResponse({"status": "error", "message": "Invalid signup details"})
    
    # Hash password and create new user
    new_user = User(
        username=request.username,
        password_hash=hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return JSONResponse({"status": "ok", "message": "Account created successfully"})
