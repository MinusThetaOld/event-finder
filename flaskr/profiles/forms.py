from flask_migrate import current
from flask_wtf import FlaskForm
from flaskr.models import Profile, User
from wtforms import (BooleanField, DateField, EmailField, PasswordField,
                     SelectField, StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)
from flask_login import current_user
from flaskr import bcrypt

# Ashiq
class ProfileInfoForm():
    pass

# Alam
class VerifyEmailForm():
    pass

# Shamsur
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type your old password"})
    
    new_password = PasswordField("New Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type a new password"})
    
    c_password = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "new_password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Retype the password"})
    
    submit = SubmitField("Save")
    
    def validate_old_password(self, odl_password):
        user = User.query.get(current_user.id)
        if not bcrypt.check_password_hash(user.password, odl_password.data):
            raise ValidationError("Password did not matched.")

class ChangePhoto():
    pass
