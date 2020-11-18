"""Database Post module"""
from django.db import models
from django.db.models import Count
from rareapi.models import Categories


class Posts(models.Model):
    """Database Post model"""
    user = models.ForeignKey("RareUsers", on_delete=models.CASCADE)

    
    # If associated category is deleted, set this Post's category to the "Uncategorized" category
    category = models.ForeignKey("Categories", on_delete=models.SET_DEFAULT, default=1)

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
    
    @property
    def reactions(self):
        """ property to access all reactions for a post and return their label and total 
        per-post count in key:val pairs
        """
        post_reactions = self.postreactions_set.all()
        return post_reactions.values('reaction__label', 'reaction__id').annotate(count=Count('reaction__id'))



    
