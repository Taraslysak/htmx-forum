from datetime import datetime
from pydantic import BaseModel

from .user import User


class RoomOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    creator: User

    class Config:
        orm_mode = True


class RoomList(BaseModel):
    items: list[RoomOut]
