from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (DateField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class CreateEventForm(FlaskForm):
    pass
