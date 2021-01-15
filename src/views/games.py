from flask import Blueprint, request, session, jsonify, abort
from flask import current_app as app
from werkzeug.security import generate_password_hash
from src.socket_server import sio
from src.db import get_db
from src.models import Game, Player
from src.views.common import get_game_by_id, get_player_by_id
from flask_socketio import emit
import secrets
import string

bp = Blueprint("games", __name__, url_prefix='/game')


@bp.route('', methods = ['POST', 'PUT'])
def create_game():
    db = get_db()
    errors = []
    data = request.get_json()
    print(data)
    name = data.get('name')
    password = data.get('password')
    player_id = data.get('creator')

    creator = Player.query.filter_by(id=player_id).first()

    if not password:
        password = generate_temp_password(8)

    if not name:
        errors.append("Name is required.")

    if not creator:
        errors.append("Need a valid Player instance as creator")

    if errors:
        app.logger.error(errors)
        return jsonify(error = errors), 400

    new_game = Game()
    new_game.name = name
    new_game.password_hash = generate_password_hash(password)
    new_game.creator = creator
    add_player_to_game(creator, new_game)
    db.add(new_game)
    db.commit()
    
    app.logger.info("A new game has been created: {}".format(new_game))
    return jsonify(game = new_game.serialize()), 201

@bp.route('/<int:game_id>/join', methods=['POST'])
def join_game(game_id):
    db = get_db()
    game = get_game_by_id(game_id)

    data = request.get_json()
    player_id = data.get('player')

    player = get_player_by_id(player_id)

    add_player_to_game(player, game)
    return jsonify(game = game.serialize()), 200

@bp.route('')
def get_all_games():
    games = Game.query.all()
    return jsonify(games = Game.serialize_list(games))

@bp.route('/<int:id>')
def get_game(id):
    game = get_game_by_id(id)
    
    return jsonify(game.serialize())

def generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

def add_player_to_game(player, game):
    game.players.append(player)
    db.add(game)
    db.commit()

    session['username'] = player.username;
    session['session_id'] = player.sid;
    sio.emit('player_joined', {'username': player.username}, room=game.id)
    app.logger.info("Player {} successfully joined game {}".format(player, game))