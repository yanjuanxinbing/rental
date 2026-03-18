from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(256), default='default.jpg')
    role = db.Column(db.Integer, default=0)  # 0=租客 1=房东 2=管理员
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    houses = db.relationship('House', backref='landlord', lazy='dynamic')
    orders = db.relationship('Order', backref='tenant', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 2

    def is_landlord(self):
        return self.role >= 1

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
