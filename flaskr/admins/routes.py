from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import bcrypt, db
from flaskr.admins.forms import *
from flaskr.models import (Complain, Notification, Profile, PromotionPending,
                           User)
from sqlalchemy import desc

admins = Blueprint("admins", __name__)


@admins.route("/admins")
@admins.route("/admins/dashboard")
@login_required
def dashboard():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    users = User.query.order_by(desc(User.created_at))[:2]
    return render_template("admins/dashboard.html", active="dashboard", users=users)


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
        "Congratulations! You are now a host. You can create events.", url_for("events.create_event"), req_pending.profile.id)
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
        "Sorry! Your request for promotion is declined.", "#", req_pending.profile.id)
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
    return render_template("admins/complain-box.html", active="complain_box")


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
    return render_template("admins/banned-users.html", active="banned_users")


@admins.route("/admins/get-profiles-by-profile-id", methods=["POST"])
@login_required
def get_profile_by_profile_id():
    if current_user.role.value != "admin":
        flash("Restricted only for admins", "danger")
        return redirect(url_for("mains.homepage"))
    id = request.form.get("get_by_profile_id")
    return redirect(url_for("profiles.view_profile", id=id))
