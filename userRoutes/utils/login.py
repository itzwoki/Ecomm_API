from passlib.context import CryptContext
from jose import jwt

from dotenv import load_dotenv
import os

from datetime import datetime,timedelta,timezone

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_TIME = 60

#hash password
def hash_password(password: str):
    return pwd_context.hash(password)

#verify password
def verify_password(plainpassword: str, hashed_password: str):
    return pwd_context.verify(plainpassword, hashed_password)

#create token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_TIME)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    