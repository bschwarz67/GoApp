from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm


from home.models import Player


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Player
        fields = UserCreationForm.Meta.fields

