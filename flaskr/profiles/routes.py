from flask import Blueprint, render_template, request
from flaskr.models import User

profiles = Blueprint("profiles", __name__)


@profiles.route("/profiles/<int:id>")
def view_profile(id: int):
    user = User.query.get(id)
    return render_template("profiles/view-profile.html", user=user)


@profiles.route("/profiles/change-info")
def change_profile_info():
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info")


@profiles.route("/profiles/change-photos")
def change_photos():
    return render_template("profiles/change-photos.html", active="change-photos")


@profiles.route("/profiles/verify-email")
def verify_email():
    return render_template("profiles/verify-email.html", active="verify-email")


@profiles.route("/profiles/change-password")
def change_password():
    return render_template("profiles/change-password.html", active="change-password")
