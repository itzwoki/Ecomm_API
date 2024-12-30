from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.orm import Session

from db.db_setup import get_db 
from db.models.user import User
from py_schemas.user import UserCreate, adminCreate, UserLogin, UserResponse, AdminResponse

from .utils.login import hash_password, verify_password, create_access_token
# from .dependencies.currentUser import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/user-singup", response_model=UserResponse)
async def user_singup(
    user: UserCreate, db: Session = Depends(get_db)
):
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already Registered."
        )
    
    hashed_password = hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password,
        role = user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/admin-signup", response_model=AdminResponse)
async def admin_signup(
    user : adminCreate,
    db: Session = Depends(get_db)
):
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exist.")
    
    hashed_password = hash_password(user.password)

    new_admin = User(
        username = user.username,
        hashed_password = hashed_password,
        role = user.role
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin

@router.post("/login")
async def login(
    user : UserLogin,
    db: Session = Depends(get_db)
):
    db_username = db.query(User).filter(User.username == user.username).first()
    if not db_username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username")
    if not verify_password(user.password, db_username.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password.")
    
    access_token = create_access_token(data={"sub": str(db_username.id)})
    return {
        "access-token" : access_token,
        "token-type": "Bearer"
    }


