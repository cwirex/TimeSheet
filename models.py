from flask_login import UserMixin
from sqlalchemy.sql import func

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    tasks = db.relationship('Task')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    date = db.Column(db.DateTime(), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
