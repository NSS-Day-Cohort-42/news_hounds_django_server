"""Database Post module"""
from django.db import models
from rareapi.models import Categories

def get_uncategorized_category_instance():
    """Get the Categories object from database that represents the "Uncategorized" category"""
    return Categories.objects.get(label='Uncategorized')

class Posts(models.Model):
    """Database Post model"""
    user = models.ForeignKey("RareUsers", on_delete=models.CASCADE)
    
    # If associated category is deleted, set this Post's category to the "Uncategorized" category
    category = models.ForeignKey("Categories", on_delete=models.SET(get_uncategorized_category_instance))

    title = models.CharField(max_length=300)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=300)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField()