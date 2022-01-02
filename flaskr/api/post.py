from flask import Blueprint, flash, jsonify, request
from flask_login import current_user, login_required
from flaskr import db
from flaskr.decorators import is_token_verified
from flaskr.models import Comment, Post, Profile, Reply, User
from flaskr.schema import (comment_schema, comment_schemas, post_schema,
                           post_schemas, reply_schema, reply_schemas)

posts = Blueprint("posts", __name__, url_prefix="/api/v1/posts")


@posts.route("", methods=["POST"])
@is_token_verified
def create():
    content = request.json.get("content")
    profile_id = request.json.get("profile_id")
    event_id = request.json.get("event_id")

    if not content or not event_id:
        return jsonify({
            "error": "Request data is not valid. Some field is missing"
        }), 400
    
    post = Post(content, None, profile_id, event_id)

    db.session.add(post)
    db.session.commit()

    return post_schema.jsonify(post), 201


@posts.route("", methods=["GET"])
def get_all():
    pass


@posts.route("/<int:id>", methods=["GET"])
def get(id: int):
    pass


@posts.route("/<int:id>", methods=["PUT"])
def update(id: int):
    pass


@posts.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    pass
