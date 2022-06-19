from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Game
from home.models import Player


def index(request, gameIdSlug=""):
	slugData = gameIdSlug.split("_")


	try:
		game = Game.objects.get(id=int(slugData[0]))
		
	except:
		#return render(request, 'home/index.html') with error message if the game the player wants isnt found
		context = {
			'error_message': "Game not found, please choose another player",
		}
		return render(request, 'home/index.html', context)
	else:
		context = {
			'game' : game,
		}
		return render(request, 'board/index.html', context)




def play(request):
	game = get_object_or_404(Game, pk=1)
	
	try:
		coordinatePlayed = request.POST['coordinate']
	
	except (KeyError):

		return render(request, 'board/index.html', {
			'game': game,
			'error_message': "You didnt select a choice.",
		})
	
	else:
		return HttpResponseRedirect(reverse('board:index'))
