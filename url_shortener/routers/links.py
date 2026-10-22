

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
import database, models
from schemas.Link import LinkCreate, LinkResponse
from utils.current_user import get_current_user
from utils.short_key_generator import generator_short_key


router = APIRouter(prefix="/links", tags=["Links"])

@router.post("/shorten", response_model=LinkResponse)
async def create_short_url(payload: LinkCreate, current_user: models.Users = Depends(get_current_user)):
    db = database.SessionLocal()

    short_key_result = generator_short_key()

    new_link = models.Link(original_url=payload.original_url, short_key=short_key_result, user_id=current_user.id)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    db.close()

    return new_link

@router.get("/{short_key}")
async def redirect_to_original(short_key: str):
    db = database.SessionLocal()

    current_original_link = db.query(models.Link).filter(models.Link.short_key == short_key).first()

    db.close()

    if current_original_link is None:
        raise HTTPException(status_code=400, detail="Такой ссылки нету.")

    current_original_link.clicks_count += 1
    db.commit()

    return RedirectResponse(url=current_original_link.original_url, status_code=307)

    
    