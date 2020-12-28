from src.db import db
from datetime import datetime

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        return '<User {} [{}]>'.format(self.username, self.id)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    players = db.relationship('Player', backref='game', lazy=True)

    def __repr__(self):
        return '<Game {} created at {}; Players: {}>'.format(self.id, self.created, len(self.players))

