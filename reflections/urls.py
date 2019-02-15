from django.urls import path

from . import views

app_name = 'reflections'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('new', views.postReflection, name='create'),
    path('details/<int:reflection_id>', views.viewReflection, name='view'),
    path('<int:reflection_id>/edit', views.editReflection, name='edit'),
    path('<int:reflection_id>/remove', views.deleteReflection, name='delete'),
]