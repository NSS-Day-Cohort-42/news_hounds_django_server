"""Database RareUser module"""
from django.db import models
from django.contrib.auth.models import User

class RareUsers(models.Model):
    """Database RareUser Model"""
    bio = models.CharField(max_length=300)
    profile_image_url = models.CharField(max_length=100)
    created_on = models.DateTimeField()
    active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)