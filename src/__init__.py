import os

from flask import Flask, jsonify
from src.admin import init_admin
from flask_cors import CORS
from src.db import init_db, get_db, create_tables
from src.model.models import Collection, Character, Tag, User, Image
from src.model.models import tags as tags_table
from src.routes import controller
from src.socket_server import init_socket_server
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
import click
import json


@click.group()
def info():
    """
    Show informations.
    """
    pass

@info.command()
@with_appcontext
def create():
    create_tables()

@info.command()
@with_appcontext
def seed():
    print("Seeding database...")

    db = get_db()
    tags_table.delete()

    tags = json.loads(open('data/tags.json').read())
    Tag.query.delete()
    for tag in tags:
        tag_model = Tag()
        tag_model.name = tag['name']
        db.add(tag_model)
        db.commit()

    collections = json.loads(open('data/collections.json').read())
    Collection.query.delete()
    db.commit()
    for collection in collections:
        collection_model = Collection()
        collection_model.name = collection['name']
        collection_model.default = collection['default']
        collection_model.tags = [Tag.query.filter_by(name=name).first() for name in collection['tags']]
        db.add(collection_model)
        db.commit()

    characters_file = json.loads(open('data/characters.json').read())
    Character.query.delete()
    for character in characters_file:
        character_model = Character()
        character_model.name = character['name']
        character_model.collection_id = Collection.query.filter_by(name=character['collection_name']).first().id
        if 'image' in character:
            image = Image(image_url=character['image']['url'], license=character['image']['license'],
                          creator=character['image']['creator'])
            character_model.image = image
            db.add(image)
        db.add(character_model)
        db.commit()

    seed_admin()


@info.command()
@with_appcontext
def seed_admin():
    print("add admin user")
    db = get_db()
    user = User()
    user.username = 'admin'
    user.password_hash = generate_password_hash(current_app.config['ADMIN_PASSWORD'])
    db.add(user)
    db.commit()


@info.command()
@with_appcontext
def config():
    """
    Show current app configuration.
    """
    for k, v in current_app.config.items():
        print("%s: %s" % (k, v))


def create_app(test_config=None):
    print("Starting app...")

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    CORS(controller.bp)

    if test_config:
        app.config.from_object(test_config)
    else:
        app.config.from_object('config')
        app.config.from_pyfile('config.py')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_db(app)
    init_socket_server(app)
    init_admin(app)

    app.cli.add_command(info)

    # register blueprints
    app.register_blueprint(controller.bp)

    return app
