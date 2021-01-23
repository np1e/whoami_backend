from flask import Blueprint, request, session, jsonify, redirect
from werkzeug.exceptions import HTTPException
from flask import current_app as app
from src.db import get_db
from src.service import game_service
from src.service.player_service import create_player
from src.service.collection_service import get_all_collections
from src.util.jwt_util import generate_token
from src.util.serialize import Serializer
from src.routes.error import build_error

bp = Blueprint("api", __name__)

@bp.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    app.logger.error(errors)
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@bp.route("/")
def index():
    return redirect("/ping", code=301)

@bp.route("/ping")
def ping():
    return jsonify("pong")

@bp.route("/collections")
def get_collections():
    collections = get_all_collections()
    return jsonify(Serializer.serialize_list(collections))

@bp.route("/game", methods=['POST'])
def create_game():
    errors = {}
    data = request.get_json()
    print(data)
    username = data.get('username')
    max_players = data.get('max_players')
    collections = data.get('collections')

    if not username:
        errors["username"] = "Username is missing"

    if not max_players:
        errors["max_players"] = "Number for maximum players is missing"

    if not collections:
        errors["collections"] = "No collections given"

    if errors:
        abort(400, description=build_error("Something went wrong.", details=errors))

    game = game_service.create_game(max_players, collections)
    token = _create_player(username, game, isCreator = True)
    
    app.logger.info("A new game has been created: {}".format(game))
    return jsonify(token=token), 201

@bp.route("/game/join", methods=['POST'])
def join_game():
    data = request.get_json()
    key = data.get('key')
    username = data.get('username')
    errors = []

    if not key:
        errors.append('No key present')
    
    if not username:
        errors.append('No username present')

    if errors:
        abort(400, description=errors)

    game = game_service.get_game(key)
    token = _create_player(username, game)

    return jsonify(token), 200

def _create_player(username, game, isCreator = False):
    player = create_player(username, game, isCreator)
    return generate_token(player._id)
