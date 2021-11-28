from flask_wtf import FlaskForm
from flaskr.models import Profile, User
from wtforms import (BooleanField, DateField, EmailField, PasswordField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


# Ashiq
class ProfileInfoForm():
    pass

# Alam
class VerifyEmailForm():
    pass

# Shamsu
class ChangePasswordForm():
    pass


class ChangePhoto():
    pass
