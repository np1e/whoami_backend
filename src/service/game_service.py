from src.model.models import Game, Collection
from src.service import save_data
from src.service.collection_service import get_collection

def create_game(max_players, collections):
    game = Game()
    game.max_players = max_players
    game.used_collections = [get_collection(collection['name']) for collection in collections]

    save_data(game)

    return game

def get_game(key):
    return Game.query.filter_by(key=key).first_or_404()
#