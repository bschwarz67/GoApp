#need to put in username for create
from django.db import models
from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from board.models import Game



class Player(AbstractUser):

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="addUserToGame", null=True)
    color = models.BooleanField(default=True)	#TRUE = white, FALSE = BLACK
    turn = models.BooleanField(default=True) #TRUE = the players turn, FALSE = not the players turn
    lastOutOfGameAction = models.DateTimeField(auto_now=True)