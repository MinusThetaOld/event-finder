from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

from flaskr import db
from flaskr.models import Role


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.profile:
            flash("Login first to access the desire route.", "danger")
            return redirect(url_for("users.login_user"))
        if current_user.role.value != Role.ADMIN.value:
            flash("Restricted for only admins.", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_host(func):
    pass


def is_general(func):
    pass


def is_unbanned(func):
    pass
