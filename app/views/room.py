from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import login_required, current_user

from app import models as m, db
from app.logger import log
from app.schema.room import RoomList


room_blueprint = Blueprint("room", __name__, url_prefix="/room")


@room_blueprint.route("/", methods=["GET"])
@login_required
def get_all():
    q = request.args.get("q", type=str, default=None)

    query = m.Room.select().order_by(m.Room.id)
    if q:
        query = m.Room.select().where(m.Room.name.ilike(f"%{q}%")).order_by(m.Room.id)

    rooms = db.session.execute(query).scalars().all()
    log(log.INFO, "Got {%i} rooms for user {%s} ", len(rooms), current_user.username)

    return render_template(
        "room/list.html",
        rooms=RoomList(items=rooms).items,
    )


@room_blueprint.route("/search", methods=["POST"])
@login_required
def search_room():
    q = request.form.get("search", type=str, default="")

    query = m.Room.select().where(m.Room.name.ilike(f"%{q}%")).order_by(m.Room.id)

    rooms = db.session.execute(query).scalars().all()
    log(
        log.INFO,
        "Searched {%i} rooms for user {%s} ",
        len(rooms),
        current_user.username,
    )

    return render_template(
        "room/list.html",
        rooms=RoomList(items=rooms).items,
        q=q,
    )


@room_blueprint.route("/new", methods=["POST"])
@login_required
def new_room():
    name = request.form.get("room-name", type=str, default=None)
    if not name:
        return ""

    room = m.Room(name=name, creator=current_user)
    room.save()

    log(log.INFO, "Created room {%s} for user {%s} ", room.name, current_user.username)

    return render_template("room/list_item.html", room=room)


@room_blueprint.route("/<int:room_id>", methods=["DELETE"])
@login_required
def delete_room(room_id):
    room = db.session.scalar(m.Room.select().where(m.Room.id == room_id))

    if not room:
        log(log.INFO, "DELETE failed. Room {%i} not found", room_id)
        return ""

    db.session.delete(room)

    db.session.commit()

    log(log.INFO, "Deleted room {%s} ", room.name)

    return ""


@room_blueprint.route("/edit-form/<int:room_id>", methods=["POST"])
@login_required
def edit_form(room_id):
    room = db.session.scalar(m.Room.select().where(m.Room.id == room_id))

    if not room:
        log(log.INFO, "POST failed. Room {%i} not found", room_id)
        return ""

    return render_template("room/edit_form.html", room=room)


@room_blueprint.route("/<int:room_id>", methods=["PUT"])
@login_required
def update_room(room_id):
    room = db.session.scalar(m.Room.select().where(m.Room.id == room_id))

    if not room:
        log(log.INFO, "PUT failed. Room {%i} not found", room_id)
        return ""

    room.name = request.form.get("room-name", type=str, default=None)
    room.save()

    log(log.INFO, "Updated room {%s} ", room.name)

    return render_template("room/list_item.html", room=room)


@room_blueprint.route("/<int:room_id>", methods=["GET"])
@login_required
def get_room(room_id):
    room = db.session.scalar(m.Room.select().where(m.Room.id == room_id))

    if not room:
        log(log.INFO, "GET failed. Room {%i} not found", room_id)
        return ""

    return render_template("room/chat/index.html", room=room)
