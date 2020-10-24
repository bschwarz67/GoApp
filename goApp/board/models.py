from django.db import models

class Game(models.Model):
	size = models.CharField(max_length=5)
	piecePositions = models.CharField(max_length=60, default='0000000000000000000000000000000000000000000000000')