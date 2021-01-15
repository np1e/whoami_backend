from src.db import db
from src.util.serialize import Serializer
from datetime import datetime

class Player(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(32))
    username = db.Column(db.String(20), unique=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    def serialize(self):
        d = Serializer.serialize(self, exclude = ['game'])
        return d

    def __repr__(self):
        return '<Player {} [{}]>'.format(self.username, self.id)

class Game(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    players = db.relationship('Player', backref='game', lazy=True)
    password_hash = db.Column(db.String())
    creator = db.relationship('Player', uselist=False)

    def serialize(self):
        d = Serializer.serialize(self, exclude = ['password_hash'])
        print(d)
        d['players'] = Player.serialize_list(self.players)
        return d

    def __repr__(self):
        return '<Game {} [{}]]>'.format(self.name, self.id)


class Character(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))

tags = db.Table('tags',
    db.Column('tag_name', db.String(20), db.ForeignKey('tag.name'), primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True)    
)

class Collection(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    characters = db.relationship('Character', backref='collection', lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('collections', lazy=True))

class Tag(db.Model, Serializer):
    name = db.Column(db.String(20), unique=True, primary_key=True)
