from flask_wtf import FlaskForm
from flaskr.models import Profile, User
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


# Ashiq
class ProfileInfoForm():
    pass

# Alam
class VerifyEmailForm(FlaskForm):
    token = StringField("Verification Token", validators=[
        DataRequired(), Length(max=6)
    ], render_kw={ "placeholder": "Enter your verification token here..." })
    save = SubmitField("Save")

# Shamsu
class ChangePasswordForm():
    pass


class ChangePhoto():
    pass
