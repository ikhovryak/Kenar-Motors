from datetime import datetime
from kondor import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), default="")
    vin_code = db.Column(db.String(30), nullable=False)
    car_model = db.Column(db.String(200), default="")
    address = db.Column(db.String(200), default="")
    car_parts = db.Column(db.Text, nullable=False)
    user_comment = db.Column(db.Text, default="")
    admin_comment = db.Column(db.Text, default="")
    date_posted = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Order('{self.first_name}', '{self.last_name}', '{self.phone}')"
