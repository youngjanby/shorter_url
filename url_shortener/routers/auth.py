from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

import database, models
from utils.password_utils import verify_password
from utils.access_token import generator_access_token
from schemas.User import TokenResponse, UserCreate, UserResponse
from utils.password_utils import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
async def login(payload: OAuth2PasswordRequestForm = Depends()):
    db = database.SessionLocal()

    current_user = db.query(models.Users).filter(models.Users.email == payload.username).first()

    if not current_user:
        db.close()
        raise HTTPException(status_code=400, detail="Пользователя не существует")


    if not verify_password(payload.password, current_user.hashed_password):
        db.close()
        raise HTTPException(status_code=400, detail="Не правильный пароль")

    token = generator_access_token(current_user.id)

    db.close()

    return {"access_token": token}

@router.post("/register", response_model=UserResponse)
async def register(payload: UserCreate):
    db = database.SessionLocal()

    if db.query(models.Users).filter(models.Users.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email уже зарегестрирован")

    hashed_pass = hash_password(payload.password)
    new_user = models.Users(email=payload.email, hashed_password=hashed_pass)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return new_user
