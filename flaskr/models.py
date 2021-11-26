import enum
from datetime import date, datetime

from flask_login import UserMixin
from itsdangerous import TimedSerializer
from itsdangerous.exc import BadTimeSignature, SignatureExpired

from flaskr import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# defining enum
class Role(enum.Enum):
    GENERAL = "general"
    HOST = "host"
    ADMIN = "admin"


class ComplainCategory(enum.Enum):
    CHEATER = "cheater"
    SCAMER = "scammer"
    HARASSMENT = "harassment"
    OTHER = "other"


# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    verified_code = db.Column(db.String)
    is_verified = db.Column(db.Boolean, default=False)
    role = db.Column(db.Enum(Role), nullable=False)
    profile = db.relationship("Profile", backref="user", uselist=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, email: str, password: str, verified_code: str, role: str) -> None:
        self.email = email
        self.password = password
        self.verified_code = verified_code
        self.role = role

    def get_reset_token(self):
        ## https://stackoverflow.com/questions/46486062/the-dumps-method-of-itsdangerous-throws-a-typeerror
        serializer = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        return serializer.dumps(self.id)
    
    @staticmethod
    def verify_reset_key(id: int, token: str, max_age=1800):
        # 1800 seconds means 30 minutes
        serializer = TimedSerializer(app.config["SECRET_KEY"], "confirmation")
        try:
            result = serializer.loads(token, max_age=max_age)
        except SignatureExpired:
            return {
                "is_authenticate": False,
                "message": "Token is expired! Please re-generate the token"
            }
        except BadTimeSignature:
            return {
                "is_authenticate": False,
                "message": "Token is not valid"
            }
        if result != id:
            return {
                "is_authenticate": False,
                "message": "Token is not valid for this user"
            }
        return {
                "is_authenticate": True,
                "message": "Token matched and not expired"
            }


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String, nullable=False)
    profile_photo = db.Column(
        db.String, default="/images/default/ProfilePhotos/default.png")
    cover_photo = db.Column(
        db.String, default="/images/default/CoverPhotos/default.png")
    rating = db.Column(db.Float, default=0.0)
    bio = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    complains = db.relationship("Complain", backref="profile")
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, first_name: str, last_name: str, date_of_birth: date, gender: str, user_id: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.user_id = user_id


class Complain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    category = db.Column(db.Enum(ComplainCategory), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    complained_by = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, text: str, complain_category, profile_id: int, complained_by: int) -> None:
        self.text = text
        self.category = complain_category
        self.profile_id = profile_id
        self.complained_by = complained_by
