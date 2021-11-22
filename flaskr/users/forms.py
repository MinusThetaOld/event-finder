from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField
from wtforms.fields.simple import BooleanField

from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets.core import CheckboxInput


# Shamsur
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[
        DataRequired()
    ], render_kw={"placeholder": "ex. Alen"})
    
    last_name = StringField("Last Name", validators=[
        DataRequired()
    ], render_kw={"placeholder": "ex. Walker"})
    
    email = StringField("Email Address", validators=[
        DataRequired()
    ], render_kw={"placeholder": "ex. alenwalker123@gmail.com"})
    
    dob = DateField("Date of Birth", validators=[
        DataRequired()
    ])
    
    gender = SelectField('Gender', choices=[(None, 'Choose a gender'),('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    
    password = StringField("Password", validators=[
        DataRequired()
    ], render_kw={"placeholder" : "Create a new password"})

    c_password = StringField("Confirm Password", validators=[
        DataRequired()
    ], render_kw={"placeholder" : "Retype the password"})
    
    submit = SubmitField("Register")
    
    condition_check= BooleanField("Agree")
    

# Ashiq
class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[
        DataRequired()
    ], render_kw={"placeholder": "ex. alenwalker123@gmail.com"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "type password here"})
    submit = SubmitField("Login")

# Alam
class ResetPassword(FlaskForm):
    pass
