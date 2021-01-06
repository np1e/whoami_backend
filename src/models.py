from src.db import db
from src.util.serialize import Serializer
from datetime import datetime

class Player(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    def serialize(self):
        d = Serializer.serialize(self)
        del d['game']

    def __repr__(self):
        return '<User {} [{}]>'.format(self.username, self.id)

class Game(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    players = db.relationship('Player', backref='game', lazy=True)
    password_hash = db.Column(db.String())
    creator = db.relationship('Player', uselist=False)

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password_hash']
        d['players'] = Serializer.serialize_list(self.players)
        return d

    def __repr__(self):
        return '<Game {} created at {}; Players: {}>'.format(self.name, self.created, len(self.players))

