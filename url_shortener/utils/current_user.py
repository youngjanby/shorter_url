from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

import database, models
from utils.access_token import SECRET_KEY

ouauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(ouauth2_scheme)) -> models.Users:
    db = database.SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="No valid code")

        user = db.query(models.Users).filter(user_id == models.Users.id).first()

        if user is None:
            raise HTTPException(status_code=401, detail="No valid code")

        return user

    except jwt.PyJWKError:
        raise HTTPException(status_code=401, detail="No valid code")
    finally:
        db.close()