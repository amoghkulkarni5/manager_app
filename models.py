from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    grow_cpu_threshold = db.Column(db.Float)
    shrink_cpu_threshold = db.Column(db.Float)
    grow_ratio = db.Column(db.Float)
    shrink_ratio = db.Column(db.Float)

class Instance(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    status = db.Column(db.Boolean, default=False, nullable=False)
    aws_id = db.Column(db.String(100))