from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import bcrypt, db
from flaskr.admins.forms import *
from flaskr.models import (Complain, Notification, Profile, PromotionPending,
                           User)

notifications = Blueprint("notifications", __name__)



@notifications.route("/notifications")
@login_required
def get_notifications():
    return render_template("notifications/notification.html")

