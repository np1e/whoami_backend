from flask_socketio import SocketIO, emit, join_room
from src.service.player_service import get_player, connect_player, disconnect_player, change_ready_state, get_player_by_session, make_guess
from src.service.game_service import start_game, advance_game, increment_next_votes, count_guess_vote
from src.util.jwt_util import get_claims
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

def emit_change(sid):
    player = get_player_by_session(sid)
    emit("player_changed", json.dumps({"player": player.serialize()}), room=player.game.key)

@sio.on('disconnect')
def disconnect():
    print('Client disconnected')
    disconnect_player(request.sid)
    emit_change(request.sid)

@sio.on('authenticate')
def on_send_auth(data):
    """Retrieves a JWT and returns the corresponding player and game"""
    token = data['token']

    # validate token signature and extract ID from token
    player_id = get_claims(token)['_id']
    if not player_id:
        return json.dumps(build_error("Invalid token"))

    player = get_player(player_id)

    if not player:
        return json.dumps(build_error("Player not found", player_id = "No match for id"))

    game = player.game
    connect_player(player_id, request.sid)
    join_room(game.key)

    emit("player_changed", json.dumps({"player": player.serialize()}), room=game.key)

    return player.serialize(), game.serialize()

@sio.on("changeReadyStatus")
def on_change_ready_state(ready):
    print(ready)
    change_ready_state(request.sid,ready)
    emit_change(request.sid)

@sio.on("startGame")
def on_start_game():
    sid = request.sid
    game = get_player_by_session(sid).game
    start_game(game)
    emit('game_started', game.serialize(), room=game.key)

@sio.on("requestGameData")
def on_request_game_data():
    sid = request.sid
    game = get_player_by_session(sid).game

    return game.serialize()

@sio.on("makeGuess")
def on_make_guess(guess):
    sid = request.sid
    player = get_player_by_session(sid)

    guessed_correctly = make_guess(player, guess)
    if guessed_correctly:
        advance_game(player.game)
        send_advance_game(player.game)

    return guessed_correctly

def send_advance_game(game):
    emit('advance_game', game.serialize(), room=game.key)

@sio.on('advanceGame')
def on_advance_game():
    game = get_player_by_session(request.sid).game
    advance_game(game)
    send_advance_game(game)

@sio.on("voteNextPlayer")
def on_vote_next():
    sid = request.sid
    game = get_player_by_session(sid).game
    voteSuccessful = increment_next_votes(game)
    emit('increment_next_vote', game.nextVotes, room=game.key)

    if voteSuccessful:
        advance_game(game)
        send_advance_game(game)

@sio.on("voteGuess")
def on_vote_guess(correct):
    sid = request.sid
    game = get_player_by_session(sid).game
    votes = count_guess_vote(player.game, correct)
    emit('change_guess_votes', json.dumps(votes), room=game.key)


