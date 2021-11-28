from flask import Blueprint, render_template, flash, redirect, url_for
from flaskr.models import User
from flaskr.profiles.forms import *
from flaskr import bcrypt, db
from flask_login import current_user

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
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info")


@profiles.route("/profiles/change-photos")
def change_photos():
    return render_template("profiles/change-photos.html", active="change-photos")


@profiles.route("/profiles/verify-email")
def verify_email():
    return render_template("profiles/verify-email.html", active="verify-email")


@profiles.route("/profiles/change-password", methods = ["POST","GET"])
def change_password():
    form=ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
        current_user.password = hashed_password
        db.session.commit()
        flash("Password changed successfully", "success")
        return redirect(url_for("profiles.change_password"))
    return render_template("profiles/change-password.html", active="change-password", form=form)
