from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.admins.forms import *
from flaskr.models import (AccountRestriction, Complain, Notification, Profile,
                           PromotionPending, Role, User)
from flaskr.notifications.utils import NotificationMessage
from sqlalchemy import desc

admins = Blueprint("admins", __name__)


@admins.route("/admins")
@admins.route("/admins/dashboard")
@login_required
def dashboard():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    users = User.query.order_by(desc(User.created_at))[:4]
    profiles = Profile.query.all()
    reqs = PromotionPending.query.all()
    data = {
        "Banned Users": 0,
        "Unverified Users": 0,
        "Host Users": 0,
        "General Users": 0,
        "Admins": 0,
    }
    for i in range(len(profiles)):
        if profiles[i].banned != None:
            data["Banned Users"] = data.get("Banned Users")+1
        if not profiles[i].user.is_verified:
            data["Unverified Users"] = data.get("Unverified Users")+1
        if profiles[i].user.role == Role.ADMIN:
            data["Host Users"] = data.get("Host Users")+1
        if profiles[i].user.role == Role.HOST:
            data["Admins"] = data.get("Admins")+1
        if profiles[i].user.role == Role.GENERAL:
            data["General Users"] = data.get("General Users")+1
        
    return render_template("admins/dashboard.html", active="dashboard", users=users, data=data)


@admins.route("/admins/pending-request")
@login_required
def pending_request():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    all_requests = PromotionPending.query.all()
    return render_template("admins/pending-request.html",
                           active="pending_request", requests=all_requests,
                           total_requests=len(all_requests))


@admins.route("/admins/pending-request/approve/<int:id>")
@login_required
def approve_pending_request(id: int):
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    req_pending = PromotionPending.query.get(id)
    if not req_pending:
        flash("Promotion object not found!", "danger")
        return redirect(url_for("admins.pending_request"))
    req_pending.approved()
    # push notification
    notification = Notification(
        NotificationMessage.approvedPromotion(), url_for("events.create_event"), req_pending.profile.id)
    db.session.add(notification)
    db.session.commit()
    flash("Profile approved.", "info")
    return redirect(url_for("admins.pending_request"))


@admins.route("/admins/pending-request/decline/<int:id>")
@login_required
def decline_pending_request(id: int):
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    req_pending = PromotionPending.query.get(id)
    if not req_pending:
        flash("Promotion object not found!", "danger")
        return redirect(url_for("admins.pending_request"))
    db.session.delete(req_pending)
    # push notification
    notification = Notification(
        NotificationMessage.declinedPromotion(), "", req_pending.profile.id)
    db.session.add(notification)   
    db.session.commit()
    flash("Profile declined.", "info")
    return redirect(url_for("admins.pending_request"))


@admins.route("/admins/complain-box")
@login_required
def complain_box():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    complains = Complain.query.all()
    return render_template("admins/complain-box.html", active="complain_box", complains=complains)


@admins.route("/admins/log")
@login_required
def log():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    return render_template("admins/log.html", active="log")


@admins.route("/admins/banned-users")
@login_required
def banned_users():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    acc_restrictions = AccountRestriction.query.all()
    total_acc_restriction = len(acc_restrictions)
    return render_template("admins/banned-users.html", active="banned_users", acc_restrictions=acc_restrictions, total_acc_restriction=total_acc_restriction)


@admins.route("/admins/get-profiles-by-profile-id", methods=["POST"])
@login_required
def get_profile_by_profile_id():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    pid = request.form.get("get_by_profile_id")
    return redirect(url_for("profiles.view_profile", id=pid))


@admins.route("/admins/get-profiles-by-user-id", methods=["POST"])
@login_required
def get_profile_by_user_id():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    uid = request.form.get("get_by_user_id")
    user = User.query.get(uid)
    if not user:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=user.profile.id))


@admins.route("/admins/get-profiles-by-email-id", methods=["POST"])
@login_required
def get_profile_by_email_id():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    email = request.form.get("get_by_email_id")
    user = User.query.filter_by(email=email).first()
    if not user:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=user.profile.id))


@admins.route("/admins/get-profiles-by-nid-id", methods=["POST"])
@login_required
def get_profile_by_nid_id():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    nid = request.form.get("get_by_nid_id")
    profile = Profile.query.filter_by(nid_number=nid).first()
    if not profile:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=profile.id))


@admins.route("/admins/ban/<int:id>", methods=["POST"])
def ban_user(id: int):
    days = request.form.get("days")
    reason = request.form.get("reason")
    try:
        expire_date = datetime.utcnow() + timedelta(days=int(days))
    except ValueError:
        flash("Enter the duration of the banned.", "danger")
        return redirect(url_for("profiles.view_profile", id=id))
    acc_restriction = AccountRestriction(expire_date, reason, id)
    db.session.add(acc_restriction)
    # push notification
    notification = Notification(NotificationMessage.ban_user(reason), url_for("mains.homepage"), id)
    db.session.add(notification)
    db.session.commit()
    flash(f"Account has been banned for {days} days.", "success")
    return redirect(url_for("profiles.view_profile", id=id))


@admins.route("/admins/unban/<int:id>")
def unban_user(id: int):
    user = User.query.get(id)
    acc_restriction = user.profile.banned
    if not acc_restriction:
        flash("User is not banned", "danger")
    else:
        db.session.delete(acc_restriction)
        # push notification
        notification = Notification(NotificationMessage.unban_user(), url_for("mains.homepage"), id)
        db.session.add(notification)
        db.session.commit()
        flash(f"The user is unbanned", "success")
    return redirect(url_for("profiles.view_profile", id=id))
