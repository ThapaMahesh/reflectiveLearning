from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('new', views.addProject, name='create'),
    path('<int:project_id>/edit', views.editProject, name='edit'),
    path('<int:project_id>/remove', views.deleteProject, name='delete'),
    path('<int:project_id>/details', views.viewProject, name='view'),

    path('<int:project_id>/add-group', views.addGroup, name='add-group'),
    path('<int:project_id>/groups/<int:group_id>/details', views.viewGroup, name='view-group'),
    path('<int:project_id>/groups/<int:group_id>/remove', views.deleteGroup, name='delete-group'),

    path('<int:project_id>/add-members', views.addMember, name='add-members'),
    path('<int:project_id>/remove-member/<int:member_id>', views.removeProjectMember, name='delete-project-member'),

    path('<int:project_id>/groups/<int:group_id>/add-members', views.addGroupMember, name='add-group-member'),
    path('<int:project_id>/groups/<int:group_id>/remove-member/<int:member_id>', views.removeGroupMember, name='delete-group-member'),
]