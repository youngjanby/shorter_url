from fastapi import APIRouter, Depends
from schemas.Link import LinkCreate, LinkResponse
from utils.current_user import get_current_user
from utils.short_key_generator import generator_short_key

import database, models

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