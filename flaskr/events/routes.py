from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.decorators import is_host
from flaskr.events.forms import *
from flaskr.models import Event, Notification, Profile, Role, User

events = Blueprint("events", __name__)


@events.route("/events/create", methods=["GET", "POST"])
@login_required
@is_host
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        flash(f"{type(form.event_max_members.data)}", "primary")
    return render_template("events/create-event.html", form=form)
