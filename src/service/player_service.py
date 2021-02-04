from src.model.models import Player
from src.service import save_data
from difflib import SequenceMatcher

def _get_similarity(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio()

def create_player(username, game, isCreator = False):
    player = Player()
    player.username = username
    player.game = game
    player.is_creator = isCreator

    save_data(player)

    return player

def connect_player(id, socket_id):
    player = get_player(id)
    player.connected = True
    player.sid = socket_id
    save_data(player)

def disconnect_player(socket_id):
    player = get_player_by_session(socket_id)
    player.connected = False
    player.ready = False
    save_data(player)

    return player

def change_ready_state(sid, ready):
    player = get_player_by_session(sid)
    player.ready = ready
    save_data(player)

def make_guess(player, guess):
    player.guesses+=1;

    if player:
        player.guessed = _get_similarity(player.character.name, guess) >= 0.85
        save_data(player)
        return player.guessed

    return False

def assign_character(player, character):
    player.character = character;
    save_data(player)

def get_player(id):
    return Player.query.filter_by(_id=id).first()

def get_player_by_session(sid):
    return Player.query.filter_by(sid=sid).first()