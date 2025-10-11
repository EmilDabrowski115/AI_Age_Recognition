from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.app import app
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.models import User
from backend.utils.password_hashing import verify_password

app = FastAPI()

class SignupRequest(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        return JSONResponse({"status": "error", "message": "Username already exists"})
    
    new_user = User(username=request.username, password_hash=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse({"status": "ok", "message": "User created successfully"})



# login endpoint request
# {
#   "username": "alice",
#   "password": "mypassword"
# }


# login endpoint response
# {
#   "status": "ok",
#   "message": "Login successful"
# }

# {
#   "status": "error",
#   "message": "Invalid credentials"
# }

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        return JSONResponse({"status": "error", "message": "Invalid credentials"})
    
    return JSONResponse({"status": "ok", "message": "Login successful"})

# signup endpoint request
# {
#   "username": "alice",
#   "password": "mypassword"
# }

# signup endpoint response
# {
#   "status": "ok",
#   "message": "User created successfully"
# }
# {
#   "status": "error",
#   "message": "Username already exists"
# }



class SignupRequest(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        return JSONResponse({"status": "error", "message": "Username already exists"})
    
    new_user = User(username=request.username, password_hash=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse({"status": "ok", "message": "User created successfully"})