from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('new', views.addProject, name='create'),
]