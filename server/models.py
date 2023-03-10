from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from datetime import datetime

db = SQLAlchemy()
migrate = Migrate(db)


class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    sid = db.Column(db.String(120))
    avatarUrl = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def toJSON(self):
        return {"id": self.id, "username": self.username, "password": self.password, "avatarUrl": self.avatarUrl, "sid": self.sid}

    def __init__(self, username, password, avatarUrl='', sid=''):
        self.username = username
        self.password = password
        self.avatarUrl = avatarUrl
        self.sid = sid

    def __repr__(self):
        return '<User %r>' % self.username


class Room(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), unique=True, nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    host_sid = db.Column(db.String, unique=True, nullable=False)
    player_sid = db.Column(db.String, unique=True)
    hostURI = db.Column(db.String)
    playerURI = db.Column(db.String)
    hostBool = db.Column(db.Boolean)
    playerBool = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def toJSON(self):
        return {"id": self.id, "room_name": self.room_name, "private": self.private, "host_sid": self.host_sid, "player_sid": self.player_sid}

    def __init__(self, room_name, private, host_sid='', player_sid=None, hostURI='', playerURI='', hostBool=False, playerBool=False):
        self.room_name = room_name
        self.private = private
        self.host_sid = host_sid
        self.player_sid = player_sid
        self.hostURI = hostURI
        self.playerURI = playerURI
        self.hostBool = hostBool
        self.playerBool = playerBool

    def __repr__(self):
        return '<Room %r>' % self.room_name


class Canvas(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(80), unique=True, nullable=False)
    svg = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def toJSON(self):
        return {"id": self.id, "theme": self.theme, "svg": self.svg}

    def __init__(self, theme, svg):
        self.theme = theme
        self.svg = svg

    def __repr__(self):
        return '<Canvas %r>' % self.theme
