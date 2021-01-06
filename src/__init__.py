import os

from flask import Flask, jsonify
from src.db import init_db
from src.models import Player
from src.views import common, games, player

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object('config')
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    init_db(app)

    app.register_error_handler(404, resource_not_found)

    # register blueprints
    app.register_blueprint(common.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(player.bp)

    return app

def resource_not_found(e):
    return jsonify(error=str(e)), 404