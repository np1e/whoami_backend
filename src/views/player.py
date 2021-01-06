from flask import Blueprint, request, session, jsonify, abort
from werkzeug.security import generate_password_hash
from src.db import get_db
from src.models import Player
import requests

bp = Blueprint("players", __name__, url_prefix="/player")

@bp.route('', methods=['POST', 'PUT'])
def create_player():
    db = get_db()
    data = request.get_json()

    username = None
    if data:
        username = data['username']

    error = None

    if not username:
        username = requests.get(url = "http://names.drycodes.com/1?separator=space").json()[0]

    if error:
        return jsonify(error=error), 400

    player = Player()
    player.username = username
    db.add(player)
    db.commit()

    return jsonify(player.serialize()), 201