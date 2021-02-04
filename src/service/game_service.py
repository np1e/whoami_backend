from src.model.models import Game, Collection, GameState
from src.service import save_data
from src.service.collection_service import get_collection
from src.service.player_service import make_guess, assign_character
from random import choice
import itertools

def create_game(max_players, collections):
    game = Game()
    game.max_players = max_players
    game.used_collections = [get_collection(collection['name']) for collection in collections]
    save_data(game)

    return game

def reset_game(game):
    game.nextVotes = 0
    game.correctGuessVotes = 0
    game.wrongGuessVotes = 0
    
    save_data(game)

def start_game(game):
    print("Start game {}".format(game.id))
    game.state = GameState.RUNNING

    for player in game.get_connected_players():
        characters = set([char for chars in [coll.characters for coll in game.used_collections] for char in chars])
        character = choice(list(characters))
        assign_character(player, character)
        characters.remove(character)

    first_player = choice(game.players)
    game.current_player = first_player
    save_data(game)

def advance_game(game):
    print("advance game")
    prev_player_index = game.players.index(game.current_player)
    game.current_player = game.players[prev_player_index+1 % len(game.players)]
    reset_game(game)
    save_data(game)

def increment_next_votes(game):
    game.nextVotes += 1
    save_data(game)
    return game.nextVotes == len(game.get_connected_players())

def count_guess_vote(game, vote):
    if vote:
        game.correctGuessVotes += 1
    else:
        game.wrongGuessVotes += 1
    save_data(game)
    
    return { 'correct': game.correctGuessVotes, 'wrong': game.wrongGuessVotes }

def _get_players_turn(game):
    for player, index in game.players.enumerate():
        if player.isOwnTurn:
            return index

def get_game(key):
    return Game.query.filter_by(key=key).first()
#