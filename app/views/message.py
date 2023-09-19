from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import login_required, current_user

from app import models as m, db
from app.logger import log
from app import schema as s


message_blueprint = Blueprint("message", __name__, url_prefix="/message")


@message_blueprint.route("/<int:room_id>", methods=["GET"])
@login_required
def get_messages_for_room(room_id):
    room = db.session.scalar(m.Room.select().where(m.Room.id == room_id))
    if not room:
        log(log.ERROR, "Room {%i} does not exist", room_id)
        return render_template("404.html"), 404

    log(
        log.INFO,
        "Got {%i} messages for room {%s} ",
        len(room.messages),
        room.name,
    )

    return render_template(
        "message/list.html",
        messages=s.MessageList(items=room.messages).items,
        room=room,
    )


@message_blueprint.route("/<int:room_id>", methods=["POST"])
@login_required
def new_message(room_id):
    room = db.session.scalar(m.Room.select().where(m.Room.id == room_id))
    if not room:
        log(log.ERROR, "Room {%i} does not exist", room_id)
        return render_template("404.html"), 404

    body = request.form.get("new_message", type=str, default=None)
    if not body:
        log(log.ERROR, "Message content cannot be empty")
        return render_template("404.html"), 404

    message = m.Message(
        body=body,
        author=current_user,
        room=room,
    )
    db.session.add(message)
    db.session.commit()

    log(log.INFO, "Created message {%s} for room {%s}", message.body, room.name)

    return render_template(
        "message/list_item.html",
        message=s.MessageOut.from_orm(message),
    )
