from flask_wtf import FlaskForm
from flaskr.models import Profile, User
from wtforms import (BooleanField, DateField, EmailField, PasswordField,
                     SelectField, StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


# Ashiq
class ProfileInfoForm(FlaskForm):
    bio =  TextAreaField("Bio", validators=[Length(max=500)],  render_kw={"placeholder": "Write your bio here..."})
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Alen"})
    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Walker"})
    dob = DateField("Date of Birth", validators=[
        DataRequired()
    ])
    save = SubmitField("Save")

# Alam
class VerifyEmailForm():
    pass

# Shamsu
class ChangePasswordForm():
    pass


class ChangePhoto():
    pass
