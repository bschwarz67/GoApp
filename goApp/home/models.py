#TODO need to put in username for create
from django.db import models
from django.contrib.auth.models import AbstractUser



class Player(AbstractUser):
    #game = models.ForeignKey(Game, on_delete=models.SET_NULL, related_name="addUserToGame", null=True)
    color = models.BooleanField(default=True)	#TRUE = white, FALSE = BLACK
    turn = models.BooleanField(default=True) #TRUE = the players turn, FALSE = not the players turn
    lastOutOfGameAction = models.DateTimeField(auto_now=True)
    opponents = models.ManyToManyField('self', symmetrical=False, related_name="+")
    challengedPlayers = models.ManyToManyField('self', symmetrical=False, related_name="+")
    challengingPlayers = models.ManyToManyField('self', symmetrical=False, related_name="+")
    previousPiecePositions = models.CharField(max_length=60, default='0000000000000000000000000000000000000000000000000')
