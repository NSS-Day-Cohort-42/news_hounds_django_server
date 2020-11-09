from django.db import models

class PostTags(models.Model):
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tags", on_delete=models.CASCADE)