from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect

def redirectToHome(request):
    return HttpResponseRedirect(reverse('home:index'))


