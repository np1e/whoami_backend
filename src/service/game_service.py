from src.model.models import Game, Collection, GameState, Vote
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
    game.nextVotes.clear()
    game.guessVotes.clear()
    game.awaitingGuessVote = False

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


def finish_game(game):
    game.state = GameState.FINISHED


def advance_game(game):
    if game.state is GameState.RUNNING:
        print("advance game")
        prev_player_index = game.players.index(game.current_player)
        guessing_players = game.get_guessing_players()
        game.current_player = guessing_players[(prev_player_index + 1) % len(guessing_players)]
        reset_game(game)
        save_data(game)


def increment_next_votes(game, player):
    game.nextVotes.append(Vote(result=True, player=player))
    save_data(game)
    return len(game.get_next_votes()) == len(game.get_connected_players()) - 1


def count_guess_vote(game, player, vote):
    new_vote = Vote(result=vote, player=player)
    game.guessVotes.append(new_vote)

    if len(game.get_correct_guess_votes()) == len(game.players) - 1:
        game.current_player.guessed = True

    if not game.get_guessing_players():
        game.state = GameState.FINISHED

    save_data(game)
    return new_vote


def _get_players_turn(game):
    for player, index in game.players.enumerate():
        if player.isOwnTurn:
            return index


def get_game(key):
    return Game.query.filter_by(key=key).first()
#
