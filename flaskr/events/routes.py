from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.events.forms import *
from flaskr.models import Event, Notification, Profile, Role, User

events = Blueprint("events", __name__)


@events.route("/events/create", methods=["GET", "POST"])
@login_required
def create_event():
    if current_user.role.value == Role.GENERAL.value:
        flash("This page is restricted for host and admins.", "danger")
        return redirect(url_for("mains.homepage"))
    form = CreateEventForm()
    return render_template("events/create-event.html", form=form)
