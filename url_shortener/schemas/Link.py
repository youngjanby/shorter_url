from datetime import datetime
from pydantic import BaseModel


class LinkCreate(BaseModel):
    original_url: str

class LinkResponse(BaseModel):
    id: int
    original_url: str
    short_key: str
    clicks_count: int
    created_at: datetime

    model_config = {"from_attributes": True}