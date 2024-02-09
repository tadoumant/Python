from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.config["SECRET_KEY"] = "62913a7dac3933f87a84626fcdeaaf9e2653f0a000843efd9bf2b31ba4767402"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gtaches.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

app.app_context().push()

login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from gtaches import routes