from flask import Flask
from flask_misaka import Misaka, markdown
from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
Misaka(app)

from app import views, models
