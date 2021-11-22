from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


# Shamsur
class RegisterForm(FlaskForm):
    pass


# Ashiq
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[
        DataRequired()
    ], render_kw={"placeholder": "ex. alenwalker123@gmail.com"})


# Alam
class ResetPassword(FlaskForm):
    pass
