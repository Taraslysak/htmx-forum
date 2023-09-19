from datetime import datetime
from pydantic import BaseModel

from .user import User


class MessageOut(BaseModel):
    id: int
    body: str
    created_at: datetime
    room_id: int
    author: User

    class Config:
        orm_mode = True


class MessageList(BaseModel):
    items: list[MessageOut]
