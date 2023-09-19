from datetime import datetime
from pydantic import BaseModel


from .user import User
from .message import MessageOut


class RoomOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    creator: User
    messages: list[MessageOut]

    class Config:
        orm_mode = True


class RoomList(BaseModel):
    items: list[RoomOut]
