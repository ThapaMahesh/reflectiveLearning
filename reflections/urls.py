from django.urls import path

from . import views

app_name = 'reflections'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('group/<int:group_id>/new', views.postReflection, name='create'),
    path('<int:reflection_id>/groups/<int:group_id>/details', views.viewReflection, name='view'),
    path('<int:reflection_id>/groups/<int:group_id>/edit', views.editReflection, name='edit'),
    path('<int:reflection_id>/groups/<int:group_id>/remove', views.deleteReflection, name='delete'),

    path('<int:reflection_id>/download', views.downloadReflection, name='download'),
    
    path('<int:reflection_id>/feedback-remove/<int:feedback_id>', views.deleteFeedback, name='delete-feedback'),
]