from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from database import engine
from routers import auth, links
import database, models

import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(links.router)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/{short_key}")
async def redirect_to_original(short_key: str):
    db = database.SessionLocal()

    current_original_link = db.query(models.Link).filter(models.Link.short_key == short_key).first()

    db.close()

    if current_original_link is None:
        raise HTTPException(status_code=400, detail="Такой ссылки нету.")

    current_original_link.clicks_count += 1
    db.commit()

    return RedirectResponse(url=current_original_link.original_url, status_code=307)