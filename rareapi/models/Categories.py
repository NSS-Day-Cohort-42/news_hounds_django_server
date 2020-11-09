"""Database category module"""
from django.db import models

class Categories(models.Model):
    """Database category model"""
    label = models.CharField(max_length=50)
