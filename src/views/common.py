from flask import Blueprint, request, session, jsonify
from src.models import Game, Player

bp = Blueprint("common", __name__)

@bp.route('/')
def index():
    return jsonify('Working')

@bp.route('/ping')
def ping():
    return jsonify('pong')

def get_player_by_id(id):
    player = Player.query.filter_by(id=id).first()

    if not player:
        abort(404, description="Player with id {} not found".format(id))
    
    return player

def get_game_by_id(id):
    game = Game.query.filter_by(id=id).first()

    if not game:
        abort(404, description="Game with id {} not found".format(id))
    
    return game

