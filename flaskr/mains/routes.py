from flask import Blueprint, redirect, render_template, request, url_for
from flaskr.users.utils import generate_token

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    return render_template("mains/homepage.html")
