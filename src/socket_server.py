from flask_socketio import SocketIO, emit, join_room
from flask import request, session
from src.db import get_db
from src.models import Player

sio = SocketIO()

def init_socket_server(app):
    print("init websocket")
    sio.init_app(app, cors_allowed_origins="*")

@sio.on('connect')
def test_connect():
    print(request.sid)
    print('Client connected')

@sio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@sio.on('join')
def join(data):
    print(data)
    db = get_db()
    id = data['player_id']

    player = Player.query.filter_by(id=id).first()
    player.sid = request.sid

    db.add(player)
    db.commit()
    join_room(data['game'])