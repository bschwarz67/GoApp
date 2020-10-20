from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse



from .models import Game


def index(request, gameIdSlug):
	
	context = {
		'game' : Game.objects.get(pk=1),
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
	
