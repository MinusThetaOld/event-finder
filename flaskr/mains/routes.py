from flask import Blueprint, render_template
from flask_login import current_user
from flaskr.models import Event
from flaskr.utils import is_eligable
from sqlalchemy import desc

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    eligable = is_eligable(current_user)
    events = Event.query.order_by(Event.event_time)[:12]
    return render_template("mains/homepage.html", eligable=eligable, events=events)
