"""Database Tag module"""
from django.db import models

class Tags(models.Model):
    """Database Tag model"""
    label = models.CharField(max_length=50)
