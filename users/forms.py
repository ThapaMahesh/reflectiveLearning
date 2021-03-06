# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
	# email = forms.CharField()
	first_name = forms.CharField()
	last_name = forms.CharField()
	norsk = forms.BooleanField(required=False)

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('first_name', 'last_name', 'username', 'norsk')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')