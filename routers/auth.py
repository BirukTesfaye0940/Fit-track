from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.user import UserCreate, UserRead, Token, UserLogin
from models.user import User
from core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
  if db_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")
  hashed_pw = hash_password(user.password)
  new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    if not user.username and not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email required"
        )

    query = db.query(User)
    if user.username:
        db_user = query.filter(User.username == user.username).first()
    else:
        db_user = query.filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

