from flask import Blueprint, redirect, render_template, request, url_for
from flaskr.users.utils import generate_token

users = Blueprint("users", __name__)

# Shamsu
@users.route("/users/register", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        # GET REQUEST
        return render_template("users/register.html")
    # POST REQUEST
    return render_template("users/register.html")


# Ashiq
@users.route("/users/login", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        # GET REQUEST
        return render_template("users/login.html")
    # POST REQUEST
    return render_template("users/login.html")


# Alam
@users.route("/users/forget_password", methods=["GET", "POST"])
def forget_password():
    if request.method == "GET":
        # GET REQUEST
        return render_template("users/forget_password.html")
    # POST REQUEST
    return render_template("users/forget_password.html")

# Alam
@users.route("/users/reset_password/<string:token>")
def reset_password(token: str):
    return redirect(url_for('login_user'))
