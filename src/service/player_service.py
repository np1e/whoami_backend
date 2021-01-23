from src.model.models import Player
from src.service import save_data

def create_player(username, game, isCreator = False):
    player = Player()
    player.username = username
    player.game = game
    player.is_creator = isCreator

    save_data(player)

    return player

def get_player(id):
    print(type(id))
    print(len(id))
    return Player.query.filter_by(_id=id).first()