#TODO:  need to check and see if cookies are allowed somewhere, playerMatch function, 
#create list for Player objects of previous aliases, allow switching. 
##
##
##

from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Player 
from django.contrib.sessions.models import Session

def index(request):
	if ('username' not in request.session):
		availablePlayers = []
		for player in Player.objects.all():
			timeSinceLastOutOfGameAction = timezone.now() - player.lastOutOfGameAction
			if((timeSinceLastOutOfGameAction.seconds <= 1200)):
				availablePlayers.append(player)
		context = {
			'opponentOptions': availablePlayers,
		}		
		if('error_message' in request.session):
			context['error_message'] = request.session['error_message']
			del request.session['error_message']
		return render(request, 'home/index.html', context) 
	else:
		if (Player.objects.get(username=request.session['username']).color): 
			availableBlackPlayers = []
			for player in Player.objects.all():
				timeSinceLastOutOfGameAction = timezone.now() - player.lastOutOfGameAction
				if((timeSinceLastOutOfGameAction.seconds <= 1200) and (not player.color) and (not player.username == request.session['username'])):
					availableBlackPlayers.append(player)
			context = {
				'opponentOptions': availableBlackPlayers,
			}		
		else: 
			availableWhitePlayers = []
			for player in Player.objects.all():
				timeSinceLastOutOfGameAction =  timezone.now() - player.lastOutOfGameAction
				if((timeSinceLastOutOfGameAction.seconds <= 1200) and (player.color) and (not player.username == request.session['username'])):
					availableWhitePlayers.append(player)
			context = {
				'opponentOptions': availableWhitePlayers,
			}
		if('error_message' in request.session):
			context['error_message'] = request.session['error_message']
			del request.session['error_message']
		return render(request, 'home/index.html', context) 


def createTempPlayer(request):
	if(Player.objects.filter(username=request.POST['name']).exists()):
		if('username' in request.session):
			if(request.session['username'] == request.POST['name']):
				Player.objects.get(username=request.session['username']).save()		
				return HttpResponseRedirect(reverse('home:index'))
			else: 
				Player.objects.get(username=request.session['username']).save()			
				request.session['error_message'] = "That username already exists, please choose another"
				return HttpResponseRedirect(reverse('home:index'))

		else:
				request.session['error_message'] = "That username already exists, please choose another"
				return HttpResponseRedirect(reverse('home:index'))
	else:
		if('username' in request.session):
			updatedPlayer = Player.objects.get(username=request.session['username'])
			updatedPlayer.username = request.POST['name']
			updatedPlayer.save()
			request.session['username'] = request.POST['name']
			return HttpResponseRedirect(reverse('home:index'))
		else:
			newPlayerUsername = request.POST['name']
			newPlayer = Player(username=newPlayerUsername)
			newPlayer.save()
			request.session['username'] = newPlayerUsername
			return HttpResponseRedirect(reverse('home:index'))




def changePlayerColor(request):
	if ('username' in request.session):
		if('color' in request.POST):
			if (request.POST['color'] == 'white'):
				updatedPlayer = Player.objects.get(username=request.session['username'])
				updatedPlayer.color = True
				updatedPlayer.save()
				return HttpResponseRedirect(reverse('home:index'))
			else:
				updatedPlayer = Player.objects.get(username=request.session['username'])
				updatedPlayer.color = False
				updatedPlayer.save()
				return HttpResponseRedirect(reverse('home:index'))
		else:
			request.session['error_message'] = "No color selected, please choose a color"
			return HttpResponseRedirect(reverse('home:index'))
	else:
		request.session['error_message'] = "No person selected, please choose a person"
		return HttpResponseRedirect(reverse('home:index'))
		

def playerMatch(request):

	return HttpResponse(request.GET.get('Method'))
