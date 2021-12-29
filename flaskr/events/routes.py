from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.decorators import is_host
from flaskr.events.forms import *
from flaskr.models import Event, Notification, Profile, Role, User
from flaskr.profiles.utils import save_photos, remove_photo
from sqlalchemy import desc

events = Blueprint("events", __name__)


@events.route("/events/create", methods=["GET", "POST"])
@login_required
@is_host
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(form.event_title.data, form.event_description.data, form.event_location.data,
                      form.event_start_time.data, form.event_days_count.data, form.event_nights_count.data,
                      form.event_fee.data, current_user.profile.id, form.event_cover_photo.data,
                      form.event_max_members.data, form.hotel_name.data, form.hotel_web_link.data)
        if form.event_cover_photo.data:
            # saving
            photo_file = save_photos(
                form.event_cover_photo.data, current_user.id, "eventCover", 1040, 260)
            event.cover_photo = "/images/uploads/eventCover/" + photo_file
        db.session.add(event)
        db.session.commit()
        flash(f"Event information saved", "success")
        return redirect(url_for("events.view_event", id=event.id))
    return render_template("events/create-event.html", form=form)


@events.route("/events")
def get_events():
    all_events = Event.query.order_by(desc(Event.created_at)).all()
    return render_template("events/events.html", events=all_events, len=len)


@events.route("/events/<int:id>")
def view_event(id: int):
    event = Event.query.get(id)
    return render_template("events/view-event.html", event=event)


@events.route("/events/settings/info/<int:id>", methods=["GET", "POST"])
@login_required
def event_info(id: int):
    event = Event.query.get(id)
    if event.host.id != current_user.profile.id:
        flash("Only the host can access this route", "danger")
        return redirect(url_for("events.view_event", id=event.id))
    form = EventForm()
    if request.method == "POST":
        # post request
        event.title = form.event_title.data
        event.description = form.event_description.data
        event.place_name = form.event_location.data
        event.event_time = form.event_start_time.data
        event.day = form.event_days_count.data
        event.night = form.event_nights_count.data
        event.fee = form.event_fee.data
        event.cover_photo = form.event_cover_photo.data
        event.hotel_name = form.hotel_name.data
        event.hotel_weblink = form.hotel_web_link.data
        if form.event_cover_photo.data:
            file_path = event.cover_photo
            if not ("/images/default/CoverPhotos/event-default.png" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.event_cover_photo.data, current_user.id, "eventCover", 1040, 260)
            event.cover_photo = "/images/uploads/eventCover/" + photo_file
        db.session.commit()
        flash(f"Event information saved", "success")
    # add the values
    elif request.method == "GET":
        form.event_title.data = event.title
        form.event_description.data = event.description
        form.event_location.data = event.place_name
        form.event_start_time.data = event.event_time
        form.event_days_count.data = event.day
        form.event_nights_count.data = event.night
        form.event_fee.data = event.fee
        form.hotel_name.data = event.hotel_name
        form.hotel_web_link.data = event.hotel_weblink
    return render_template("events/event-info.html", active="event-info", form=form, event=event)


@events.route("/events/settings/plans/<int:id>", methods=["GET", "POST"])
@login_required
def event_plans(id: int):
    event = Event.query.get(id)
    if event.host.id != current_user.profile.id:
        flash("Only the host can access this route", "danger")
        return redirect(url_for("events.view_event", id=event.id))
    form = EventPlansForm()
    if form.validate_on_submit():
        # post request
        pass
    # add the values
    return render_template("events/edit-plans.html", active="event-plans", form=form, event=event)
