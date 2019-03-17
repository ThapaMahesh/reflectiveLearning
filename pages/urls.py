# users/urls.py
from django.urls import path
from . import views

app_name = "pages"
urlpatterns = [
	path('', views.home, name="home"),
	path('dashboard', views.index, name='dashboard'),
	path('search', views.search, name='search'),
	path('contact-developer', views.send_email, name='email'),
]