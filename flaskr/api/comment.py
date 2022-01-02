from flask import Blueprint, flash, request
from flask_login import current_user, login_required
from flaskr import db
from flaskr.decorators import is_host, is_verified
from flaskr.models import Comment, Post, Profile, Reply

comments = Blueprint("comment", __name__, url_prefix="/api/v1/comments")


@comments.route("", methods=["POST"])
def create():
    pass


@comments.route("", methods=["GET"])
def get_all():
    pass


@comments.route("/<int:id>", methods=["GET"])
def get(id: int):
    pass


@comments.route("/<int:id>", methods=["PUT"])
def update(id: int):
    pass


@comments.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    pass
