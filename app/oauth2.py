from jose import JWTError , jwt
from datetime import datetime,timedelta
from schemas import user
from sqlalchemy.orm import Session
import models
from database import get_db
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')
#SECRET KEY
SECRET_KEY = settings.secret_key 
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
print(ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credential_exception):
     try:
         payload = jwt.decode(token,SECRET_KEY,algorithms = ALGORITHM)
         email = payload.get("user_email")
         permissions = payload.get("permissions") 
         if email is None:
             raise credential_exception
         token_data = user.TokenData(email=email,permissions=permissions) 
     #import this from your respective schemas
     except JWTError:
         raise credential_exception
     
     return token_data
     
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, credential_exception)
    current_user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if not current_user:
        raise credential_exception
    return current_user
    
     
def get_current_active_superuser(current_user:models.User = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Not enough permissions")
    return current_user
    
    
def sign_up_new_user(db, email: str, password: str):
    user = db.query(models.User).filter(models.User.email==email).first();
    if user:
        return False  # User already exists
    new_user = create_user(
        db,
        schemas.UserCreate(
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
        ),
    )
    return new_user