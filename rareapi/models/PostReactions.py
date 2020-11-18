from django.db import models
from django.db import models
from rareapi.models import RareUsers, Reactions, Posts

""" Model for PostReactions bridge table """

class PostReactions(models.Model):
    user = models.ForeignKey("RareUsers", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reactions", on_delete=models.CASCADE)
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)