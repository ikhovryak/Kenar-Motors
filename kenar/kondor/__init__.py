from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

app.config['SECRET_KEY'] = "b26af5b375735ecd4078ae6a32c3ea6c"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.google.mail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
from kondor import routes

# Part 10: 26:44
