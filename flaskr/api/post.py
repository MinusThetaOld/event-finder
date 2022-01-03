from flask import Blueprint, flash, jsonify, request
from flask_login import current_user, login_required
from jwt.exceptions import InvalidTokenError
from flaskr import db, app
from flaskr.decorators import is_token_verified
from flaskr.models import Comment, Event, Post, Profile, Reply, User
from flaskr.schema import (comment_schema, comment_schemas, post_schema,
                           post_schemas, reply_schema, reply_schemas)
from jwt import decode

posts = Blueprint("posts", __name__, url_prefix="/api/v1/posts")

def get_user():
    jwt_token = request.headers.get("Authorization")
    if not jwt_token:
        return jsonify({
            "error": "JTW token is missing."
        }), 403
    try:
        data = decode(jwt_token, app.config.get(
            "JWT_SECRET_KEY"), algorithms=['HS256'])
        return data.get("id")
    except InvalidTokenError:
        return jsonify({
            "error": "Invalid token.",
        }), 403
    except Exception as e:
        return jsonify({
            "error": e.__str__(),
        }), 500

@posts.route("", methods=["POST"])
@is_token_verified
def create():
    content = request.json.get("content")
    profile_id = request.json.get("profile_id")
    event_id = request.json.get("event_id")

    profile = Profile.query.get(profile_id)
    event = Event.query.get(event_id)
    
    if not content or not event_id or not profile:
        return jsonify({
            "error": "Request data is not valid. Some field is missing."
        }), 400
    
    if profile.id not in event.members and profile.id != event.host.id:
        return jsonify({
            "error": "Only members or host can post in this event."
        }), 401
    
    post = Post(content, None, profile.id, event.id)

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
@is_token_verified
def delete(id: int):
    user_id = get_user()
    profile = User.query.get(user_id).profile
    post = Post.query.get(int(id))
    if not profile or not post:
        return jsonify({
            "error": "Profile or post not found."
        }), 404
    if profile.id!=post.profile.id:
        return jsonify({
            "error": "You can't delete this post."
        }), 406
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({
        "message": "Successfully deleted the post"
        }), 200