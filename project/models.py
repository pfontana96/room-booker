from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Reservation(db.Model):
    __tablename__ = 'user_room'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), primary_key=True)
    date_time = db.Column(db.DateTime, primary_key=True)

    user = db.relationship('User', back_populates='rooms')
    room = db.relationship('Room', back_populates='users')

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(30))
    name = db.Column(db.String(100))

    rooms = db.relationship('Reservation', back_populates='user')

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    capacity = db.Column(db.Integer)

    users = db.relationship('Reservation', back_populates='room')
