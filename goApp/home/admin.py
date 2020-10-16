from django import forms
from django.contrib.auth.forms import UserCreationForm


from home.models import Player


class CustomUserCreationForm(UserCreationForm):

    #username = forms.RegexField(regex="^[0-9a-zA-Z]*$", max_length=10)

    class Meta(UserCreationForm.Meta):
        model = Player
        #fields = ('password1', 'password2', 'username')
        fields = UserCreationForm.Meta.fields
