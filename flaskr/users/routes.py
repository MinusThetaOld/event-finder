import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_login import login_user as login_user_function
from flask_login import logout_user as logout_user_function
from flaskr import bcrypt, db
from flaskr.mails import send_mail
from flaskr.models import Profile, Role, User
from flaskr.users.forms import *
from flaskr.users.utils import generate_token, password_reset_key_mail_body

users = Blueprint("users", __name__)


@users.route("/users/register", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Generating token
        generated_token_for_email = generate_token(6)
        # Hashing
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        hashed_token = bcrypt.generate_password_hash(
            generated_token_for_email).decode("utf-8")
        # Creating user
        all_users = User.query.all()
        user = None
        if len(all_users) == 0:
            user = User(form.email.data, hashed_password,
                        hashed_token, Role.ADMIN)
        else:
            user = User(form.email.data, hashed_password,
                        hashed_token, Role.GENERAL)
        db.session.add(user)
        db.session.commit()
        # Creating profile
        profile = Profile(form.first_name.data, form.last_name.data,
                          form.dob.data, form.gender.data, user.id)
        db.session.add(profile)
        db.session.commit()
        # Sending email
        send_mail(user.email, "Email Verification Code",
                  f"Your Token is {generated_token_for_email}")
        fetched_user = User.query.filter_by(id=user.id).first()
        flash(
            f"Account created for {fetched_user.profile.first_name} {fetched_user.profile.last_name}", "success")
        return redirect(url_for("users.login_user"))
    return render_template("users/register.html", form=form, active='register')


@users.route("/users/login", methods=["GET", "POST"])
def login_user():
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        # Fetching the user
        fetched_user = User.query.filter_by(email=form.email.data).first()
        # Checking the email and password
        if fetched_user and bcrypt.check_password_hash(fetched_user.password, form.password.data):
            login_user_function(fetched_user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            flash("Login Successfull.", "success")
            return redirect(next_page) if next_page else redirect(url_for('mains.homepage'))
        else:
            flash("Login Failed! Please Check Email and Password.", "danger")
    return render_template("users/login.html", form=form, active='login')


@users.route("/users/logout")
@login_required
def logout_user():
    logout_user_function()
    return redirect(url_for("users.login_user"))


@users.route("/users/forget_password", methods=["GET", "POST"])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # Fetching the user
        user = User.query.filter_by(email=form.email.data).first()
        # Sending email
        send_mail(user.email, "Password Reset Token",
                  password_reset_key_mail_body(user.id, user.get_reset_token(), int(os.getenv("EXPIRE_TIME"))))
        flash(f"Check your email to continue.", "primary")
        return redirect(url_for('users.login_user'))
    return render_template("users/forget_password.html", form=form)


@users.route("/users/reset_password/<int:id>/<string:token>", methods=["GET", "POST"])
def reset_password(id: int, token: str):
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    # Verifying the token
    veridication_result = User.verify_reset_key(
        id, token, int(os.getenv("EXPIRE_TIME")))
    if not veridication_result["is_authenticate"]:
        return render_template("mains/errors.html", status=400, message=f"{veridication_result['message']}")
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User.query.get(id)
        user.password = hashed_password
        db.session.commit()
        flash(f"{veridication_result['message']}", "success")
        return redirect(url_for("users.login_user"))
    return render_template("users/reset_password.html", form=form)


@users.route("/users/view-profile")
@login_required
def view_user_profile():
    return redirect(url_for("profiles.view_profile", id=current_user.id))
