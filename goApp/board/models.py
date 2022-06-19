from django.db import models
import home.models


class Game(models.Model):
	size = models.CharField(max_length=5)
	piecePositions = models.CharField(max_length=60, default='0000000000000000000000000000000000000000000000000')
	whitePlayer = models.ForeignKey(home.models.Player, on_delete=models.CASCADE, related_name="+", null=True)
	blackPlayer = models.ForeignKey(home.models.Player, on_delete=models.CASCADE, related_name="+", null=True)
	movingPlayer = models.ForeignKey(home.models.Player, on_delete=models.CASCADE, related_name="+", null=True)
	