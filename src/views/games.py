from flask import Blueprint, request, session, jsonify, abort
from werkzeug.security import generate_password_hash
from src.db import get_db
from src.models import Game, Player
import secrets
import string

bp = Blueprint("games", __name__, url_prefix='/game')


@bp.route('', methods = ['POST', 'PUT'])
def create_game():
    db = get_db()
    errors = []
    data = request.get_json()
    print(data)
    name = data['name']
    password = data['password']
    player_id = data['creator']

    creator = Player.query.filter_by(id=player_id).first()

    if not password:
        password = generate_temp_password(8)

    if not name:
        errors.append("Name is required.")

    if not creator:
        errors.append("Need a valid Player instance as creator")

    if errors:
        return jsonify(error = errors), 400

    new_game = Game()
    new_game.name = name
    new_game.password_hash = generate_password_hash(password)
    new_game.creator = creator
    new_game.players.append(creator)
    db.add(new_game)
    db.commit()
    print(new_game)
    return jsonify(game = new_game.serialize()), 201

@bp.route('')
def get_all_games():
    games = Game.query.all()
    return jsonify(games = Game.serialize_list(games))

@bp.route('/<int:id>')
def get_game_by_id(id):
    game = Game.query.filter_by(id=id).first()

    if game is None:
        abort(404, description="Game with id {} not found".format(id))
        
    return jsonify(game.serialize())

def generate_temp_password(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))