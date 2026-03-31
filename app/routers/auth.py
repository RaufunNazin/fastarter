# 1. Update your imports
from fastapi import Depends, status, APIRouter, HTTPException, Body
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import Token
# NEW: Import bcrypt directly and remove the utils import
import bcrypt
from .. import models, oauth2

router = APIRouter()

# NEW: Define the verification logic directly in the file to match register
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

@router.post("/login", response_model=Token, tags=['auth'])
def login_user(user_credentials: dict = Body(...), db: Session = Depends(get_db)):
    username = user_credentials.get("username")
    password = user_credentials.get("password")

    if username is None or password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username and password are required")

    user = db.query(models.User).filter(models.User.email == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user found with this email")

    # NEW: Call the local verify_password function instead of utils.verify_password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    access_token = oauth2.create_access_token({"id": user.id, "email": user.email})
    return {
        "access_token": access_token,
        "token_type": "Bearer",
     }