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

    @property
    def fullname(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def username(self):
        return f"{self.user.username}"

    @property
    def is_staff(self):
        return self.user.is_staff

    @property
    def authors_following(self):
        """Property to easily access list of authors as RareUsers that user is currently subscribed to"""
        # get QuerySet of subscription objects where this RareUser is the `follower` that are active
        # (active subscription == subscription where ended_on is None)
        active_subscriptions = self.follows_subscriptions.filter(ended_on__isnull=True)

        # return list of just the author RareUsers objects for those subscriptions
        return [ subscription.author for subscription in active_subscriptions ]
    
    @property
    def email(self):
        return f"{self.user.email}"

    @property
    def post_count(self):
        """Property returning the count of posts this RareUser has created"""

        # you can access all of the Posts where the user foreign key
        # points to "this" user via self.posts_set
        return len(self.posts_set.all())
