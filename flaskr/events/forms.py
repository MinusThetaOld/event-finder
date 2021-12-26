from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (DateField, StringField, SubmitField,
                     TextAreaField, IntegerField)
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class CreateEventForm(FlaskForm):
    event_title = StringField("Event Title*", validators=[
        DataRequired(), Length(max=150, min=2)
    ], render_kw={"placeholder": "Enter a title of the event."})
    event_location = StringField("Event Location*", validators=[
        DataRequired(), Length(max=100, min=2)
    ], render_kw={"placeholder": "ex. City, Country."})
    event_start_time = DateField("Event Start Time*", validators=[
        DataRequired()
    ])
    event_max_members = IntegerField("Maximum Members*", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Enter the maximum number."})
    event_description = TextAreaField("Description*", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Tell about the event."})
    event_days_count = IntegerField("Number of days*", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Event days"})
    event_night_count = IntegerField("Number of nights*", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Event nights"})
    hotel_name = StringField("Hotel Name", render_kw={"placeholder": "Enter the name of hotel if the event includes it."})
    hotel_web_link = StringField("Hotel web link", render_kw={"placeholder": "Enter the link of hotel. Such as facebook page link, booking.com link etc."})
    event_cover_photo = FileField("Event Cover Photo", validators=[
                            FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Create the event")
    
    
    
