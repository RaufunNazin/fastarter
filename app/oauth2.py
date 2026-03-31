from jose import JWTError, jwt
# Added timezone to imports
from datetime import datetime, timedelta, timezone 
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import models
from .database import SessionLocal
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_TIME = 60 * 60 * 24 * 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def create_access_token(data : dict) :
    to_encode = data.copy()
    # Swapped utcnow() for now(timezone.utc) and changed minutes to seconds
    expire_time = datetime.now(timezone.utc) + timedelta(seconds = EXPIRATION_TIME)
    to_encode.update({ "exp" : expire_time })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credentials_exception) :
    try :
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("id")
        email = payload.get("email")
    
        if not id :
            raise credentials_exception
        token_data = schemas.TokenData(id = id, email = email)
    except JWTError :
        raise credentials_exception
    return token_data
    
def get_current_user(token : str = Depends(oauth2_scheme)) :
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                          detail = "error",
                                          headers = { "WWW-authenticate" : "Bearer"}
                                          )
    token_data = verify_access_token(token, credentials_exception)
    return token_data

# Added db argument and removed SessionLocal usage. Changed 401 to 403 (standard for role rejections).
def check_authorization(user, db) :
    user_from_db = db.query(models.User).filter(models.User.id == user.id).first()
    if user_from_db.role != 1 :
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Unauthorized Access")
    return user_from_db