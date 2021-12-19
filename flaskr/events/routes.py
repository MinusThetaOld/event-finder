from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import bcrypt, db
from flaskr.admins.forms import *
from flaskr.models import (Complain, Notification, Profile, PromotionPending,
                           User)

events = Blueprint("events", __name__)


@events.route("/events", methods=["GET", "POST"])
@login_required
def create_event():
    pass
