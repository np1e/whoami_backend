from src.db import db
from src.util.serialize import Serializer
from datetime import datetime
import string
import random
import uuid
from flask_login import UserMixin

KEY_LENGTH = 16
UUID_LENGTH = 36

def generate_key():
    symbols = list(string.ascii_lowercase) + [str(i) for i in list(range(9))]
    key = ''.join(random.choice(symbols) for i in range(KEY_LENGTH))
    print(key)
    return key

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(18), nullable=False, unique=True)
    password_hash = db.Column(db.String(64))

    # Required for administrative interface
    def __unicode__(self):
        return self.username

class Player(db.Model, Serializer):
    _id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    username = db.Column(db.String(20), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    connected = db.Column(db.Boolean, default = False)
    is_creator = db.Column(db.Boolean)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character', backref="assigned_players")

    def serialize(self):
        d = Serializer.serialize(self, exclude = ['game'])
        return d

    def __repr__(self):
        return '<Player {} [{}]>'.format(self.username, self._id)

class Game(db.Model, Serializer):
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid, unique=True)
    key = db.Column(db.String(KEY_LENGTH), unique=True, default=generate_key)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    state = db.Column(db.String(32), default="waiting")
    players = db.relationship('Player', backref='game', lazy=True, cascade="all, delete")
    max_players = db.Column(db.Integer)

    def serialize(self):
        d = Serializer.serialize(self)
        print(d)
        d['players'] = Player.serialize_list(self.players)
        return d

    def __repr__(self):
        return '<Game {}>'.format(self.id)


class Character(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'))

    def __repr__(self):
        return '{}'.format(self.name)

tags = db.Table('tags',
    db.Column('tag_name', db.String(20), db.ForeignKey('tag.name'), primary_key=True),
    db.Column('collection_id', db.Integer, db.ForeignKey('collection.id'), primary_key=True)    
)

class Collection(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=generate_uuid)
    name = db.Column(db.String(30), unique=True, nullable=False)
    characters = db.relationship('Character', backref='collection', lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery', backref=db.backref('collections', lazy=True), cascade="all, delete", passive_deletes=True)
    default = db.Column(db.Boolean, default = False)

    def serialize(self):
        d = Serializer.serialize(self)
        d['amountOfCharacters'] = len(self.characters)

        return d

    def __repr__(self):
        return '{}'.format(self.name)

class Tag(db.Model, Serializer):
    name = db.Column(db.String(20), unique=True, primary_key=True, nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)
