# users/urls.py
from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('password_change/', views.change_password, name='password_change'),
    path('find-members/', views.findUsers, name='findUser'),
]