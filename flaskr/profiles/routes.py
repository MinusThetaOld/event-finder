from flask import Blueprint, redirect, render_template, request, url_for
from flask.helpers import flash
from flask_login import current_user, login_required
from flaskr import bcrypt, db
from flaskr.models import User
from flaskr.profiles.forms import *
from flaskr.profiles.utils import remove_photo, save_photos

profiles = Blueprint("profiles", __name__)


@profiles.route("/profiles/<int:id>")
def view_profile(id: int):
    user = User.query.get(id)
    if not user:
        return render_template("mains/errors.html", status=404, message="User not found!")
    return render_template("profiles/view-profile.html", user=user)


@profiles.route("/profiles/settings/change-info", methods=["GET", "POST"])
@login_required
def change_profile_info():
    form = ProfileInfoForm()
    if form.validate_on_submit():
        current_user.profile.bio = form.bio.data
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.date_of_birth = form.dob.data
        db.session.commit()
        flash("Profile information updated successfully.", "success")
        return redirect(url_for("profiles.change_profile_info"))
    elif request.method == "GET":
        form.bio.data = current_user.profile.bio
        form.first_name.data = current_user.profile.first_name
        form.last_name.data = current_user.profile.last_name
        form.dob.data = current_user.profile.date_of_birth
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info", form=form)


@profiles.route("/profiles/settings/change-photos", methods=["GET", "POST"])
@login_required
def change_photos():
    form = ChangePhoto()
    if form.validate_on_submit():
        if form.profile_photo.data:
            # deleting
            file_path = current_user.profile.profile_photo
            if not ("/images/default/ProfilePhotos/default.png" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.profile_photo.data, current_user.id, "profile", 250, 250)
            current_user.profile.profile_photo = "/images/uploads/profile/" + photo_file
            db.session.commit()
        if form.cover_photo.data:
            # deleting
            file_path = current_user.profile.cover_photo
            if not ("/images/default/CoverPhotos/default.png" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.cover_photo.data, current_user.id, "cover", 1040, 260)
            current_user.profile.cover_photo = "/images/uploads/cover/" + photo_file
            db.session.commit()
    return render_template("profiles/change-photos.html", active="change-photos", form=form)


@profiles.route("/profiles/settings/verify-email", methods=["GET", "POST"])
@login_required
def verify_email():
    form = VerifyEmailForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.verified_code, form.token.data):
            flash("Token did not matched!", "danger")
        else:
            current_user.verified_code = None
            current_user.is_verified = True
            db.session.commit()
            flash("Email verified successfully!=.", "success")
        return redirect(url_for("profiles.verify_email"))
    return render_template("profiles/verify-email.html", active="verify-email", form=form)


@profiles.route("/profiles/settings/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.new_password.data).decode("utf-8")
        current_user.password = hashed_password
        db.session.commit()
        flash("Password changed successfully.", "success")
        return redirect(url_for("profiles.change_password"))
    return render_template("profiles/change-password.html", active="change-password", form=form)


@profiles.route("/profiles/settings/remove-cover-photo")
@login_required
def remove_cover_photo():
    if not ("/images/default/CoverPhotos/default.png" in current_user.profile.cover_photo):
        remove_photo(current_user.profile.cover_photo)
        current_user.profile.cover_photo = "/images/default/CoverPhotos/default.png"
        db.session.commit()
        flash("Cover photo removed.", "success")
    else:
        flash("Cannot remove default cover photo.", "danger")
    return redirect(url_for("profiles.change_photos"))


@profiles.route("/profiles/settings/remove-profile-photo")
@login_required
def remove_profile_photo():
    if not ("/images/default/ProfilePhotos/default.png" in current_user.profile.profile_photo):
        remove_photo(current_user.profile.profile_photo)
        current_user.profile.profile_photo = "/images/default/ProfilePhotos/default.png"
        db.session.commit()
        flash("Profile photo removed.", "success")
    else:
        flash("Cannot remove default profile photo.", "danger")
    return redirect(url_for("profiles.change_photos"))


@profiles.route("/profiles/settings/connections", methods=["GET", "POST"])
@login_required
def change_connections():
    form = ChangeConnections()
    return render_template("profiles/change-connections.html", active="change-connections", form=form)
