import os

from flask import Flask, jsonify
from flask_cors import CORS
from src.db import init_db
from src.views import common, games, player
from src.socket_server import init_socket_server, sio

def resource_not_found(e):
    return jsonify(error=str(e)), 404

def create_app(test_config = None):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins="http://localhost:8080")

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

    app.register_error_handler(404, resource_not_found)

    # register blueprints
    app.register_blueprint(common.bp)
    app.register_blueprint(games.bp)
    app.register_blueprint(player.bp)

    return app
