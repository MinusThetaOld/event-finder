import enum
from datetime import date, datetime

from flaskr import db


# defining enum
class Role(enum.Enum):
    GENERAL = "general"
    HOST = "host"
    ADMIN = "admin"



# Models
class User(db.Model):
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
    complains = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    
    def __init__(self, first_name: str, last_name: str, date_of_birth: date, gender: str, user_id: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.user_id = user_id
