from flask_socketio import SocketIO, emit, join_room
from src.service.player_service import get_player
from src.util.jwt_util import get_claims
from src.db import get_db
from flask import request
import json
from src.routes.error import build_error

sio = SocketIO()

def init_socket_server(app):
    print("init websocket")
    sio.init_app(app, cors_allowed_origins="*")

@sio.on('connect')
def test_connect():
    print(request.sid)
    print('Client connected')

@sio.on('disconnect')
def disconnect():
    print('Client disconnected')
    emit("player_disconnected")

@sio.on('authenticate')
def send_auth(data):
    """Retrieves a JWT and returns the corresponding player and game"""
    token = data['token']

    # validate token signature and extract ID from token
    player_id = get_claims(token)['_id']
    if not player_id:
        return json.dumps(build_error("Invalid token"))

    player = get_player(player_id)
    player.connected = True
    db = get_db()
    db.add(player)
    db.commit()

    if not player:
        return json.dumps(build_error("Player not found", player_id = "No match for id"))

    game = player.game
    emit("player_joined", {"player": player.serialize()}, room=game.key)
    join_room(game.key)

    return json.dumps({"player": player.serialize(), "game": game.serialize()})

def start_game(key):
    sio.emit("game_started", room=key)