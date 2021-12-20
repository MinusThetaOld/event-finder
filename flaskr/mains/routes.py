from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from flaskr.utils import is_eligable

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    eligable = is_eligable(current_user)
    return render_template("mains/homepage.html", eligable=eligable)
