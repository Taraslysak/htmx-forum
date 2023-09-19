import sqlalchemy as sa

from datetime import datetime
from sqlalchemy import orm
from typing import TYPE_CHECKING

from app.database import db

from .utils import ModelMixin


if TYPE_CHECKING:
    from .user import User

    # from .message import Message


class Room(db.Model, ModelMixin):
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), unique=True, nullable=False
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.utcnow
    )

    creator_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("users.id"), nullable=False
    )

    creator: orm.Mapped["User"] = orm.relationship()
    # messages: orm.Mapped[list["Message"]] = orm.relationship()
