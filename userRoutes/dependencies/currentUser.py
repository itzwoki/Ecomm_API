from fastapi import HTTPException,Depends, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from db.models.user import User
from db.db_setup import get_db

from dotenv import load_dotenv
import os 

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
        token : str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        print(f"Received Token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token.")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    return user

def check_admin(
        token : str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    admin_check = get_current_user(token, db)
    if admin_check.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission Denied"
        )
    return admin_check