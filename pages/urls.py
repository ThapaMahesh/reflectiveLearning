# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('dashboard', views.index, name='dashboard'),
	path('myreflections', views.reflections, name='myreflections'),
]