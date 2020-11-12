"""Database Post module"""
from django.db import models
from rareapi.models import Categories


class Posts(models.Model):
    """Database Post model"""
    user = models.ForeignKey("RareUsers", on_delete=models.CASCADE)

    def get_uncategorized_category_instance():
        """Get the Categories object from database that represents the "Uncategorized" category"""
        return Categories.objects.get(label='Uncategorized')
    
    # If associated category is deleted, set this Post's category to the "Uncategorized" category
    category = models.ForeignKey("Categories", on_delete=models.SET(get_uncategorized_category_instance))

    title = models.CharField(max_length=300)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=300)
    content = models.CharField(max_length=1000)
    approved = models.BooleanField()

    @property
    def tags(self):
        """Property to access each post's associated tag instances
        
        posttags_set is a queryset of posttags objects for which the post instance 
        (aka self)'s primary key exists as that posttag's "post_id" foreign key
        """
        
        post_tags = self.posttags_set.all()
        return [ pt.tag for pt in post_tags]
    
    
