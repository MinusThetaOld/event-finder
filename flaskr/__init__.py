import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flaskr import users

load_dotenv()


# create and configure the app
app = Flask(__name__)

# secret keys
app.secret_key = os.getenv("SECRET_KEY")

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_SERVER')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "static/images/uploads"

# database
db = SQLAlchemy(app)

# Migration
migrate = Migrate(app, db)

from flaskr.mains.routes import mains
from flaskr.profiles.routes import profiles
from flaskr.users.routes import users

# Registering blueprints
app.register_blueprint(users)
app.register_blueprint(profiles)
app.register_blueprint(mains)
