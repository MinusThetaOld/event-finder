from flask import Blueprint, flash, request
from flask_login import current_user, login_required
from flaskr import db
from flaskr.decorators import is_host, is_verified
from flaskr.models import Comment, Post, Profile, Reply

replies = Blueprint("replies", __name__, url_prefix="/api/v1/replies")


@replies.route("", methods=["POST"])
def create():
    pass


@replies.route("", methods=["GET"])
def get_all():
    pass


@replies.route("/<int:id>", methods=["GET"])
def get(id: int):
    pass


@replies.route("/<int:id>", methods=["PUT"])
def update(id: int):
    pass


@replies.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    pass
