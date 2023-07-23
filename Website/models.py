from Website import db
from flask_login import UserMixin
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(500))
    date = db.Column(db.DateTime(), default=datetime.utcnow()) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    notes = db.relationship('Note')

