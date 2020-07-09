from django.shortcuts import render
from django.http import HttpResponse
from opponentSelect.models import Player
from django.template import loader


def index(request):
	p = Player(name="James")
	p.save()

	players = ""

	for x in Player.objects.all():
		players += x.__str__()
		players += " "
	
	return HttpResponse("lol")


# Create your views here.
