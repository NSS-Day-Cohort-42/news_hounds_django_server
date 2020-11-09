"""Database PostTag module"""
from django.db import models

class PostTags(models.Model):
    """Database PostTag Model"""
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tags", on_delete=models.CASCADE)