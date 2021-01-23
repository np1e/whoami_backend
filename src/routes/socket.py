from src.socket_server import sio
from src.service.player_service import get_player
from src.util.jwt_util import get_claims
import json
from src.routes.error import build_error

@sio.on('connect')
def test_connect():
    print(request.sid)
    print('Client connected')

@sio.on('disconnect')
def disconnect():
    print('Client disconnected')
    emit("player_disconnected")

@sio.on('authenticate')
def send_auth():
    """Retrieves a JWT and returns the corresponding player and game"""
    token = data['token']
    print("Authenticate with token {}".format(token))

    # validate token signature and extract ID from token
    player_id = get_claims(token)
    if not player_id:
        return json.dumps(build_error("Invalid token"))

    player = get_player(player_id)

    if not player:
        return json.dumps(build_error("Player not found", player_id = "No match for id"))

    game = player.game
    join_room(game.key)

    emit("player_joined", {"player": player}, room=game.key)

    return player, player.game

def start_game(key):
    sio.emit("game_started", room=key)