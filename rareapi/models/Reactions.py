from django.db import models
from django.db.models.fields.files import ImageField

class Reactions(models.Model):
    label = models.CharField(max_length=50)
    image_url = models.ImageField(upload_to='reactions', height_field=None, width_field=None, null=True, max_length=None)
