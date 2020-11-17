"""Database Subscriptions module"""
from django.db import models

class Subscriptions(models.Model):
    """Database Subscriptions Model"""
    follower = models.ForeignKey("RareUsers", on_delete=models.CASCADE, related_name="follows_subscriptions")
    author = models.ForeignKey("RareUsers", on_delete=models.CASCADE, related_name="following_subscriptions")
    created_on = models.DateTimeField()
    ended_on = models.DateTimeField(blank=True, null=True)
