from flask import Blueprint, render_template, request
from flaskr.models import User

profiles = Blueprint("profiles", __name__)


@profiles.route("/profiles/<int:id>")
def view_profile(id: int):
    user = User.query.get(id)
    return render_template("profiles/view-profile.html", user=user)
