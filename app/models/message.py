import sqlalchemy as sa

from datetime import datetime
from sqlalchemy import orm
from typing import TYPE_CHECKING

from app.database import db


if TYPE_CHECKING:
    from .room import Room
    from .user import User


class Message(db.Model):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    body: orm.Mapped[str] = orm.mapped_column(sa.String(1024), nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.utcnow
    )

    room_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("room.id"), nullable=False
    )
    author_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False
    )

    room: orm.Mapped["Room"] = orm.relationship(backref="messages")
    author: orm.Mapped["User"] = orm.relationship(backref="messages")
