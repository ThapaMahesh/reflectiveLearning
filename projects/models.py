from django.db import models
from thesis_prj import settings
from datetime import datetime


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(default=datetime.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_projects")

    def __str__(self):
        return self.slug


class Group(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_groups")
	name = models.CharField(max_length=50)
	created_at = models.DateTimeField(default=datetime.now)
	members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Member')


class Member(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_members")
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_members")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_members")
	joined_date = models.DateTimeField(default=datetime.now)
