# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name="home"),
	path('dashboard', views.index, name='dashboard'),
	path('myreflections', views.reflections, name='myreflections'),
	path('contact-developer', views.send_email, name='email'),
]