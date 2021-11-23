from flask_wtf import FlaskForm
from flaskr.models import Profile, User
from wtforms import (BooleanField, DateField, EmailField, PasswordField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Alen"})

    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Walker"})

    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "ex. alenwalker123@gmail.com"})

    dob = DateField("Date of Birth", validators=[
        DataRequired()
    ])

    gender = SelectField('Gender', choices=[(
        None, 'Choose a gender'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Create a new password"})

    c_password = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Retype the password"})

    submit = SubmitField("Register")

    condition_check = BooleanField("Agree", validators=[DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "ex. alenwalker123@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)],
                             render_kw={"placeholder": "type password here"})
    submit = SubmitField("Login")


class ForgetPassword(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "Enter your associated email address"})
    submit = SubmitField("Send Email")


class ResetPassword(FlaskForm):
    pass
