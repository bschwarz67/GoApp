from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def redirectToHome(request):
    return HttpResponsePermanentRedirect(reverse('home:index'))


