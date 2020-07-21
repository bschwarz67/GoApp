#TODO: error checking for color selection, display opponent lists properly, need to check and see if cookies are allowed somewhere, playerMatch function


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Player 
from django.contrib.sessions.models import Session

def index(request):
	
	if ('username' not in request.session):
		context = {
			'opponentOptions': Player.objects.all(),
		}
		return render(request, 'home/index.html', context) 
	else:
		if (Player.objects.get(username=request.session['username']).color): 
			context = {
				'opponentOptions': Player.objects.filter(color=False),
			}		
		else: 
			context = {
				'opponentOptions': Player.objects.filter(color=True),
			}	
		return render(request, 'home/index.html', context) 


def createPlayer(request):
	
	if(Player.objects.filter(username=request.POST['name']).exists()):
		if('username' in request.session):
			if(request.session['username'] == request.POST['name']):
				return render(request, 'home/index.html')
			else: 
				return render(request, 'home/index.html', { 'error_message': "That username already exists, please choose another", })
		else:
			return render(request, 'home/index.html', { 'error_message': "That username already exists, please choose another", })
	else:
		if('username' in request.session):
			updatedPlayer = Player.objects.get(username=request.session['username'])
			updatedPlayer.username = request.POST['name']
			updatedPlayer.save()
			request.session['username'] = request.POST['name']
			return render(request, 'home/index.html') 
		else:
			newPlayerUsername = request.POST['name']
			newPlayer = Player(username=newPlayerUsername)
			newPlayer.save()
			request.session['username'] = newPlayerUsername
			return render(request, 'home/index.html') 




def changePlayerColor(request):
	if ('username' in request.session):
		selectedColor = request.POST['color']
		Player.objects.get(username=request.session['username']).color = selectedColor
		return render(request, 'home/index.html') 
	else:
		return render(request, 'home/index.html', { 'error_message': "You haven't chosen a username yet, please choose one before continuing", })
		

def playerMatch(request):

	return HttpResponse(request.GET.get('Method'))
