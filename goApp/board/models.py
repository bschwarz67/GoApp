from django.db import models

class Game(models.Model):
	playerOne = models.CharField(max_length=100)	
	playerTwo = models.CharField(max_length=100)
	size = models.CharField(max_length=5)
	piecePositions = models.CharField(max_length=60, default='0000000000000000000000000000000000000000000000000')

# Create your models here.
