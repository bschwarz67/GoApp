from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from home.admin import CustomUserCreationForm
from home.models import Player 

def signup(request):
	
	if (request.method == 'POST'):
		form = CustomUserCreationForm(request.POST)
		if (form.is_valid()):
			#process data
			print(form.cleaned_data['password2'])
			player = Player.objects.create_user(form.cleaned_data['username'], email=None, password=form.cleaned_data['password2'])
			player.save()
			return HttpResponseRedirect(reverse('home:index'))
	else:

		form = CustomUserCreationForm()
	
	return render(request, 'registration/signup.html', {'form': form,})

