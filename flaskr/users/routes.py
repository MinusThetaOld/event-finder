from flask import Blueprint, flash, redirect, render_template, request, url_for
from flaskr import bcrypt, db
from flaskr.models import Profile, Role, User
from flaskr.users.forms import *
from flaskr.users.utils import generate_token
import flask_login as fl

users = Blueprint("users", __name__)


@users.route("/users/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        # generating token
        generated_token_for_email = generate_token(6)
        # hashing
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        hashed_token = bcrypt.generate_password_hash(
            generated_token_for_email).decode("utf-8")
        # creating user
        user = User(form.email.data, hashed_password,
                    hashed_token, Role.GENERAL)
        db.session.add(user)
        db.session.commit()
        # creating profile
        profile = Profile(form.first_name.data, form.last_name.data,
                          form.dob.data, form.gender.data, user.id)
        db.session.add(profile)
        db.session.commit()
        fetched_user = User.query.filter_by(id=user.id).first()
        flash(
            f"Account created for {fetched_user.profile.first_name} {fetched_user.profile.last_name}", "success")
        return redirect(url_for("users.login_user"))
    return render_template("users/register.html", form=form, active='register')


@users.route("/users/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        fetched_user = User.query.filter_by(email=form.email.data).first()
        if fetched_user and bcrypt.check_password_hash(fetched_user.password, form.password.data):
            fl.login_user(fetched_user, remember=form.remember_me.data)
            flash("Login Successfull!", "success")
            return redirect(url_for('mains.homepage'))
        else:
            flash("Login Failed! Invalid Credentials.", "danger") 
    return render_template("users/login.html", form=form, active='login')


@users.route("/users/logout")
def logout_user():
    return redirect(url_for("users.login_user"))


@users.route("/users/forget_password", methods=["GET", "POST"])
def forget_password():
    form = ForgetPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Email sending
        # @TODO
        flash(f"A verification link is sent to '{user.email}'", "primary")
        return redirect(url_for('users.login_user'))
    return render_template("users/forget_password.html", form=form)


@users.route("/users/reset_password/<string:token>")
def reset_password(token: str):
    return redirect(url_for('login_user'))
