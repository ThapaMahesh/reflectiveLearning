from django.db import models
# from django.contrib.auth.models import User
from projects.models import Group
from thesis_prj import settings
from datetime import datetime


EXP_CHOICES = (
    (1, 'Yes'),
    (0, 'No'),
)

class Reflection(models.Model):
	title = models.CharField(max_length=255, default="")
	tags = models.CharField(max_length=255, default="")
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reflections")
	# group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_reflections")
	is_group = models.BooleanField()
	created_at = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.title


class Discussion(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_discussions")
    reflection = models.ForeignKey(Reflection, on_delete=models.CASCADE, related_name="reflection_discussions")
    feedback = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)


class Prompts(models.Model):
	reflection = models.ForeignKey(Reflection, on_delete=models.CASCADE, related_name="reflection_prompts")
	situation = models.TextField()
	has_experience = models.BooleanField(choices=EXP_CHOICES)
	experience = models.TextField()
	experience_helpful = models.TextField()
	factors = models.TextField()
	emotions = models.TextField()
	solutions = models.TextField()
	learnings = models.TextField()
	current = models.BooleanField(choices=EXP_CHOICES)
	readability = models.TextField()
	wordFrequency = models.TextField(default='')
	sentiment = models.FloatField(default=0.0)
	updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_prompts")
	created_at = models.DateTimeField(default=datetime.now)
	updated_at = models.DateTimeField(default=datetime.now)