from flask import Blueprint, render_template
from flaskr.models import User
import datetime
from flaskr.profiles.forms import *

profiles = Blueprint("profiles", __name__)


@profiles.route("/profiles/<int:id>")
def view_profile(id: int):
    user = User.query.get(id)
    if not user:
        return render_template("mains/errors.html", status=404, message="User not found!")
    join_date = user.created_at.strftime("%B, %Y")
    return render_template("profiles/view-profile.html", user=user, join_date=join_date)


@profiles.route("/profiles/change-info")
def change_profile_info():
    form = ProfileInfoForm()
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info", form=form)


@profiles.route("/profiles/change-photos")
def change_photos():
    return render_template("profiles/change-photos.html", active="change-photos")


@profiles.route("/profiles/verify-email")
def verify_email():
    return render_template("profiles/verify-email.html", active="verify-email")


@profiles.route("/profiles/change-password")
def change_password():
    return render_template("profiles/change-password.html", active="change-password")
