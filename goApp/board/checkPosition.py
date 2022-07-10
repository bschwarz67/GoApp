from home.models import Player
from board.models import Game


class Check:
    def __init__(self, newPosition=''):
        self.position = newPosition

    def checkPlayValidity(self):
        print(Game.objects.get(id=1).piecePositions)
        return