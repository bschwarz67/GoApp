#TODO:  need to check and see if cookies are allowed somewhere,
#create list for Player objects of previous aliases, allow switching.
#figure out how to save every time user does out of game action, think changePlayerColor and the challenges

#for views.index.html, could there be a bette rway to keep track of currently challenged players and opponents for preventing
#more than on challenge?

#can you challengers players when theyre not in home.index in their browser?

from django.contrib.auth import login
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Player
from board.models import Game



def index(request):
	if request.user.is_authenticated:
		availablePlayers = []
		challengedPlayers = []
		challengingPlayers = []
		opponents = []
		opponentObjects = []
		ids = []

		for player in Player.objects.all():
			timeSinceLastOutOfGameAction = timezone.now() - player.lastOutOfGameAction
			if timeSinceLastOutOfGameAction.days < 1:
				if timeSinceLastOutOfGameAction.seconds <= 1200 and not player.username == request.user.username:
					availablePlayers.append(player.username)
		
		
		for x in Player.objects.all():
			ids.append(x.id)

		for x in request.user.challengedPlayers.all():
			challengedPlayers.append(x.username)
		
		for x in request.user.challengingPlayers.all():
			challengingPlayers.append(x.username)

		for x in request.user.opponents.all():
			opponents.append(x.username)
		
		for x in Game.objects.all():
			opponent = {}
			if request.user.username == x.whitePlayer.username or request.user.username == x.blackPlayer.username:
				if(request.user.username == x.whitePlayer.username):
					opponent['value'] = x.blackPlayer.username
				else:
					opponent['value'] = x.whitePlayer.username
				opponent['gameId'] = x.id
				opponentObjects.append(opponent)
		
		context = {
			'availablePlayers': availablePlayers,
			'challengedPlayers': challengedPlayers,
			'challengingPlayers': challengingPlayers,
			'opponentObjects': opponentObjects,
			'opponents': opponents,
			'ids': ids,
		}
		if 'error_message' in request.session:
			context['error_message'] = request.session['error_message']
			del request.session['error_message']

		return render(request, 'home/index.html', context)

	else:
		availablePlayers = []
		for player in Player.objects.all():
			timeSinceLastOutOfGameAction = timezone.now() - player.lastOutOfGameAction
			if timeSinceLastOutOfGameAction.days < 1:
				if timeSinceLastOutOfGameAction.seconds <= 1200:
					availablePlayers.append(player.username)
		context = {
			'availablePlayers': availablePlayers,
		}
		if 'error_message' in request.session:
			context['error_message'] = request.session['error_message']
			del request.session['error_message']

		return render(request, 'home/index.html', context)



def createTempPlayer(request):
	if(Player.objects.filter(username=request.POST['name']).exists()):
		if(request.user.is_authenticated):
			if(request.user.username == request.POST['name']):
				Player.objects.get(username=request.user).save()
				return HttpResponseRedirect(reverse('home:index'))
			else:
				Player.objects.get(username=request.user).save()
				request.session['error_message'] = "That username already exists, please choose another"
				return HttpResponseRedirect(reverse('home:index'))
		else:
			request.session['error_message'] = "That username already exists, please choose another"
			return HttpResponseRedirect(reverse('home:index'))
	else:
		if(request.user.is_authenticated):
			updatedPlayer = Player.objects.get(username=request.user)
			#updatedPlayer.username = request.POST['name']
			updatedPlayer.save()
			return HttpResponseRedirect(reverse('home:index'))
		else:
			newPlayerUsername = request.POST['name']
			newPlayer = Player(username=newPlayerUsername)
			newPlayer.save()
			login(request, newPlayer)
			return HttpResponseRedirect(reverse('home:index'))




def changePlayerColor(request):
	if (request.user.is_authenticated):
		if('color' in request.POST):
			if (request.POST['color'] == 'white'):
				updatedPlayer = Player.objects.get(username=request.user)
				updatedPlayer.color = True
				updatedPlayer.save()
				return HttpResponseRedirect(reverse('home:index'))
			else:
				updatedPlayer = Player.objects.get(username=request.user)
				updatedPlayer.color = False
				updatedPlayer.save()
				return HttpResponseRedirect(reverse('home:index'))
		else:
			request.session['error_message'] = "No color selected, please choose a color"
			return HttpResponseRedirect(reverse('home:index'))
	else:
		request.session['error_message'] = "No person selected, please choose a person"
		return HttpResponseRedirect(reverse('home:index'))
