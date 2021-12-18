from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import bcrypt, db
from flaskr.admins.forms import *
from flaskr.models import Complain, Profile, PromotionPending, User

admins = Blueprint("admins", __name__)


@admins.route("/admins")
@admins.route("/admins/dashboard")
def dashboard():
    return render_template("admins/dashboard.html", active="dashboard")


@admins.route("/admins/pending-request")
def pending_request():
    all_requests = PromotionPending.query.all()
    return render_template("admins/pending-request.html", active="pending_request", requests=all_requests, pending_req_numbers=len(all_requests))


@admins.route("/admins/complain-box")
def complain_box():
    return render_template("admins/complain-box.html", active="complain_box")


@admins.route("/admins/log")
def log():
    return render_template("admins/log.html", active="log")


@admins.route("/admins/banned-users")
def banned_users():
    return render_template("admins/banned-users.html", active="banned_users")
