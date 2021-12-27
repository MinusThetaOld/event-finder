from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import bcrypt, db
from flaskr.admins.forms import BanUserForm
from flaskr.decorators import is_general, is_unbanned, is_verified
from flaskr.models import (Complain, Notification, Profile, PromotionPending,
                           Role, SocialConnection, User)
from flaskr.notifications.utils import NotificationMessage
from flaskr.profiles.forms import *
from flaskr.profiles.utils import remove_photo, save_photos

profiles = Blueprint("profiles", __name__, url_prefix="/profiles")


@profiles.route("/<int:id>")
@login_required
@is_unbanned
def view_profile(id: int):
    ban_user_form = BanUserForm()
    user = User.query.get(id)
    if not user:
        return render_template("mains/errors.html", status=404, message="User not found!")
    return render_template("profiles/view-profile.html", user=user, ban_form=ban_user_form)


@profiles.route("/settings/change-info", methods=["GET", "POST"])
@login_required
@is_unbanned
def change_profile_info():
    form = ProfileInfoForm()
    if form.validate_on_submit():
        current_user.profile.bio = form.bio.data
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.date_of_birth = form.dob.data
        current_user.profile.nid_number = form.nid.data
        db.session.commit()
        flash("Profile information updated successfully.", "success")
        return redirect(url_for("profiles.change_profile_info"))
    elif request.method == "GET":
        form.bio.data = current_user.profile.bio
        form.first_name.data = current_user.profile.first_name
        form.last_name.data = current_user.profile.last_name
        form.dob.data = current_user.profile.date_of_birth
        form.nid.data = current_user.profile.nid_number
    return render_template("profiles/edit-profile-info.html", active="edit-profile-info", form=form)


@profiles.route("/settings/change-photos", methods=["GET", "POST"])
@login_required
@is_unbanned
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


@profiles.route("/settings/verify-email", methods=["GET", "POST"])
@login_required
@is_unbanned
def verify_email():
    form = VerifyEmailForm()
    if form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.verified_code, form.token.data):
            flash("Token did not matched!", "danger")
        else:
            current_user.verified_code = None
            current_user.is_verified = True
            db.session.commit()
            flash("Email verified successfully.", "success")
        return redirect(url_for("profiles.verify_email"))
    return render_template("profiles/verify-email.html", active="verify-email", form=form)


@profiles.route("/settings/change-password", methods=["GET", "POST"])
@login_required
@is_unbanned
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


@profiles.route("/settings/remove-cover-photo")
@login_required
@is_unbanned
def remove_cover_photo():
    if not ("/images/default/CoverPhotos/default.png" in current_user.profile.cover_photo):
        remove_photo(current_user.profile.cover_photo)
        current_user.profile.cover_photo = "/images/default/CoverPhotos/default.png"
        db.session.commit()
        flash("Cover photo removed.", "success")
    else:
        flash("Cannot remove default cover photo.", "danger")
    return redirect(url_for("profiles.change_photos"))


@profiles.route("/settings/remove-profile-photo")
@login_required
@is_unbanned
def remove_profile_photo():
    if not ("/images/default/ProfilePhotos/default.png" in current_user.profile.profile_photo):
        remove_photo(current_user.profile.profile_photo)
        current_user.profile.profile_photo = "/images/default/ProfilePhotos/default.png"
        db.session.commit()
        flash("Profile photo removed.", "success")
    else:
        flash("Cannot remove default profile photo.", "danger")
    return redirect(url_for("profiles.change_photos"))


@profiles.route("/settings/connections", methods=["GET", "POST"])
@login_required
@is_unbanned
def change_connections():
    form = ChangeConnections()
    if form.validate_on_submit():
        if current_user.profile.social_links == None:
            social = SocialConnection(form.facebook.data, form.twitter.data, form.github.data,
                                      form.linkedin.data, form.website.data, current_user.profile.id)
            db.session.add(social)
        else:
            current_user.profile.social_links.facebook = form.facebook.data
            current_user.profile.social_links.twitter = form.twitter.data
            current_user.profile.social_links.github = form.github.data
            current_user.profile.social_links.linkedin = form.linkedin.data
            current_user.profile.social_links.website = form.website.data
        db.session.commit()
        flash("Connection information updated successfully.", "success")
        return redirect(url_for("profiles.change_connections"))
    elif request.method == "GET":
        form.facebook.data = current_user.profile.social_links.facebook if current_user.profile.social_links else None
        form.twitter.data = current_user.profile.social_links.twitter if current_user.profile.social_links else None
        form.github.data = current_user.profile.social_links.github if current_user.profile.social_links else None
        form.linkedin.data = current_user.profile.social_links.linkedin if current_user.profile.social_links else None
        form.website.data = current_user.profile.social_links.website if current_user.profile.social_links else None
    return render_template("profiles/change-connections.html", active="change-connections", form=form)


@profiles.route("/request_for_host")
@login_required
@is_unbanned
@is_general
def req_for_host():
    if current_user.profile.nid_number == None \
            or current_user.profile.nid_number == "":
        flash("Please add NID number in profile.", "danger")
        return redirect(url_for("mains.homepage"))
    is_pending = PromotionPending.query.filter_by(
        profile_id=current_user.profile.id).first()
    if is_pending:
        flash("Already requested for being host. Please wait for respose.", "danger")
        return redirect(url_for("mains.homepage"))
    # All ok
    new_pending_req = PromotionPending(current_user.profile.id)
    db.session.add(new_pending_req)
    # push notification
    users = User.query.filter_by(role=Role.ADMIN).all()
    for u in users:
        notification = Notification(
            NotificationMessage.want_promotion(
                current_user.profile.get_fullname()),
            url_for("admins.pending_request"),
            u.profile.id
        )
        db.session.add(notification)
    db.session.commit()
    flash("A request has been sent. Wait for the response from admins.", "success")
    return redirect(url_for("mains.homepage"))


@profiles.route("/complains")
@login_required
@is_unbanned
@is_verified
def view_complains():
    complains = None
    active = None
    if request.args.get("complains_by") == "self":
        complains = Profile.query.get(current_user.profile.id).complains
        active = "self"
    else:
        complains = Complain.query \
            .filter_by(complain_for=current_user.profile.id).all()
    return render_template("profiles/complains.html", complains=complains, active=active)


@profiles.route("/bookmark/<int:id>")
@login_required
@is_unbanned
def bookmark_profile(id: int):
    list_of_bookmark = []
    bookmarks = current_user.profile.profile_bookmarks
    if bookmarks and id in bookmarks:
        flash("Profile already bookmarked.", "danger")
    else:
        if not bookmarks:
            list_of_bookmark.append(id)
        else:
            for i in range(len(bookmarks)):
                list_of_bookmark.append(bookmarks[i])
            list_of_bookmark.append(id)
        current_user.profile.profile_bookmarks = list_of_bookmark
        db.session.commit()
        flash("Added to your profile bookmark", "success")
    return redirect(url_for("profiles.view_profile", id=id))


@profiles.route("/unbookmark/<int:id>")
@login_required
@is_unbanned
def unbookmark_profile(id: int):
    list_of_bookmark = []
    bookmarks = current_user.profile.profile_bookmarks
    if bookmarks and id not in bookmarks:
        flash("Not in bookmark list.", "danger")
    else:
        for i in range(len(bookmarks)):
            if bookmarks[i] != id:
                list_of_bookmark.append(bookmarks[i])
        current_user.profile.profile_bookmarks = list_of_bookmark
        db.session.commit()
        flash("Remove from your profile bookmark", "success")
    return redirect(url_for("profiles.view_profile", id=id))
