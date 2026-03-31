from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import User, ResponseUser, Token
# REMOVE passlib import: from passlib.context import CryptContext
import bcrypt # ADD direct bcrypt import
from .. import models, oauth2
from ..oauth2 import check_authorization

router = APIRouter()

# --------------------------------------------------------------------------
# 1. NEW HASHING FUNCTION
# --------------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hashes a password using bcrypt directly, bypassing passlib."""
    # bcrypt requires bytes, so we encode the string
    pwd_bytes = password.encode('utf-8')
    # Generate the salt and hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Return as a decoded string for database storage
    return hashed_password.decode('utf-8')

@router.post("/register", status_code = 201, response_model = Token, tags=['user'])
def create_user(user : User ,db : Session = Depends(get_db)) :
    # REMOVE passlib context: pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # check for same email or username
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username unavailable")
        
    print(f"Hashed Password: {user.password}")
    
    # USE our custom function instead of passlib
    hashed_pass = hash_password(user.password)
    user.password = hashed_pass
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = oauth2.create_access_token({ "id": new_user.id, "email": new_user.email })
    return {"access_token": access_token, "token_type": "Bearer" }

@router.get("/me", response_model=ResponseUser, tags=['user'])
def get_info(db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    return user_from_db

@router.get("/users", tags=['user'])
def get_users(db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    # Pass the existing db session into the authorization function
    check_authorization(user, db)
    users = db.query(models.User).all()
    return users