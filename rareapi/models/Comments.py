from django.db import models

class Comments(models.Model):
    post = models.ForeignKey("Posts", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    subject = models.CharField(max_length=100)
    created_on = models.DateTimeField()
    