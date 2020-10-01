from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from home.admin import CustomUserCreationForm
from home.models import Player 
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model

def signup(request):
	
	if (request.method == 'POST'):
		form = CustomUserCreationForm(request.POST)
		if (form.is_valid()):
			#process data
			print(form.cleaned_data['password2'])
			Player = get_user_model()
			player = Player.objects.create_user(form.cleaned_data['username'], form.cleaned_data['password2'])
			player.save()
			return HttpResponseRedirect(reverse('home:index'))
	else:

		form = CustomUserCreationForm()
	
	return render(request, 'registration/signup.html', {'form': form,})

