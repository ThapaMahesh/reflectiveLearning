# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
import json

from .forms import CustomUserCreationForm
from .models import CustomUser

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def findUsers(request):
	email = request.GET.get('search', '')
	if(email == ""):
		return JsonResponse({})
	users = CustomUser.objects.filter(email__icontains = email)
	# return JsonResponse(serializers.serialize('json', users), safe=False)
	data = []
	for eachUser in users:
		data.append({'id': eachUser.id, 'text': eachUser.first_name + ' (' + eachUser.email + ')'})

	json_data = {"results": data, "pagination": {"more": False}}
	return JsonResponse(json_data, safe=False)