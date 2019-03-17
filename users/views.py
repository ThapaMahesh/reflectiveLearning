# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core import serializers
import json

from .forms import CustomUserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return HttpResponseRedirect(reverse('dashboard'))
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'registration/change_password.html', {
			'form': form
		})


def findUsers(request):
	username = request.GET.get('search', '')
	if(username == ""):
		return JsonResponse({})
	users = CustomUser.objects.filter(username__icontains = username)
	# return JsonResponse(serializers.serialize('json', users), safe=False)
	data = []
	for eachUser in users:
		data.append({'id': eachUser.id, 'text': eachUser.first_name + ' (' + eachUser.username + ')'})

	json_data = {"results": data, "pagination": {"more": False}}
	return JsonResponse(json_data, safe=False)